from cffi import FFI


ffi = FFI()
ffi.cdef('''
void* VW_InitializeA(char *);

void* VW_ReadExampleA(void*, char*);

float VW_Predict(void*, void*);

void VW_FinishExample(void*, void*);

void VW_Finish(void*);
''')
ffilib = ffi.verify('''
typedef short char16_t;
#define bool int
#define true (1)
#define false (0)

#include "vwdll.h"
''',
     include_dirs=['/usr/include/vowpalwabbit/', '/usr/local/include/vowpalwabbit', './vw_cffi', '/usr/include', '.', '/srv/rtb/rtb/optimization'],
     library_dirs=['/usr/lib', '/usr/lib64'],
     libraries=['vw_c_wrapper', "vw", "allreduce"],
     ext_package='vw'
)


class VWModelError(Exception):
    pass


class EmptyVWModel(object):
    """ Object instance used while VWModel is loaded and initialized
    """
    def __init__(self):
        """bidlog expects this field to be available right after bidder starts"""
        self.model_id = ""

    def getScore(self, example_str):
        return 0

    def calibrateScore(self, raw_score):
        return 0

    def close(self):
        pass


class VWCFFIWrapper(object):
    """
    Base class - allows to get predicted score only
    Make predictions using Vowpal Wabbit.

    `vw_cmd` - command line options for initializing VW instance
    Example usage:
    >>> vw = VWCFFIWrapper("/usr/bin/vw -t -i /path/to/vw_file --quiet")
    >>> value = vw.getScore("query string")
    >>> vw.close()
    """
    def __init__(self, vw_cmd):
        self._vw = ffilib.VW_InitializeA(vw_cmd)
        if not self._vw:
            raise VWModelError("VW Model failed to init: '%s'" % vw_cmd)

    def __del__(self):
        self.close()

    def close(self):
        if self._vw:
            ffilib.VW_Finish(self._vw)
            self._vw = None

    def getScore(self, example_str):
        """Call VW with the `example_str` and return the uncalibrated result.
        :type example_str: unicode
        :return float
        """
        example_str = example_str.encode("ascii", "ignore")
        example = ffilib.VW_ReadExampleA(self._vw, example_str)
        score = ffilib.VW_Predict(self._vw, example)
        ffilib.VW_FinishExample(self._vw, example)
        return score



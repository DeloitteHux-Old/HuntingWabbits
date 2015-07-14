import os

from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    long_description = readme.read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy"
]

setup(
    name="huntingwabbits",
    packages=find_packages(),
    setup_requires=["vcversioner"],
    install_requires=["characteristic", "Twisted"],
    entry_points={
        "console_scripts": [
            "vw-server = huntingwabbits.cli:main",
            "vw-client = huntingwabbits.client:main",
        ],
    },
    vcversioner={"version_module_paths": ["huntingwabbits/_version.py"]},
    author="Magnetic Engineering",
    author_email="Engineering@Magnetic.com",
    classifiers=classifiers,
    description="Interface to VW optimization models",
    license="MIT",
    long_description=long_description,
    url="https://github.com/Magnetic/HuntingWabbits",
)

import setuptools
from distutils.core import Extension
from Cython.Build import cythonize
import numpy

with open("README.md", "r") as fh:
    long_description = fh.read()

# module extension
ext = Extension("bdata.mudpy",
                sources=["./bdata/mudpy.pyx",
                         "./mud_src/mud.c",
                         "./mud_src/mud_gen.c",
                         "./mud_src/mud_fort.c",
                         "./mud_src/mud_encode.c",
                         "./mud_src/mud_all.c",
                         "./mud_src/mud_tri_ti.c",
                         "./mud_src/mud_misc.c",
                         "./mud_src/mud_new.c"],
                include_dirs=['./mud_src/'])

setuptools.setup(
    name="bdata",
    version="5.1.1",
    author="Derek Fujimoto",
    author_email="fujimoto@phas.ubc.ca",
    description="BNMR/BNQR MUD file reader and asymmetry calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dfujim/bdata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Cython",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Development Status :: 5 - Production/Stable",
    ],
    install_requires=['cython>=0.28','numpy>=1.14','requests>=2.22.0',
                      'pandas>=0.25'],
    ext_modules = cythonize([ext],include_path =[numpy.get_include()]),
)


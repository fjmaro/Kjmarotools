"""Package information"""

# pylint: disable=line-too-long
__all__ = ["__title__", "__summary__", "__uri__", "__version__",
           "__author__", "__email__", "__license__", "__copyright__",
           "PYTHON_REQUIRES", "INSTALL_REQUIRES", "CLASSIFIERS"]


# Package title, version, short description and repository URL
__title__ = "kjmarotools"
__version__ = "0.1.1"
__summary__ = "Python tools for photo, media management and other purposes"
__uri__ = f"https://github.com/fjmaro/{__title__.capitalize()}"  # Github Projet capitalized

# Author, email, license and copyright
__email__ = ""
__author__ = "Francisco José Mata Aroco"
__license__ = "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
__copyright__ = f"2022 {__author__}"

# Python and package requirements
PYTHON_REQUIRES = ">=3.9, <4"
INSTALL_REQUIRES: list = []

# PyPI classifiers with '__license__' included (https://pypi.org/classifiers/)
CLASSIFIERS = [__license__,
               "Topic :: Multimedia",
               "Intended Audience :: Developers",
               "Programming Language :: Python :: 3",
               "Development Status :: 3 - Alpha", ]

"""Setup PyImpuyte package."""

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyImpuyte",
    version="1.3.4",
    author="Marcus Suresh, Ronnie Taib",
    author_email="marcus.suresh@industry.gov.au, marcus.suresh@data61.csiro.au, ronnie.taib@data61.csiro.au",
    description="Intelligent imputation using tree-based and machine learning algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.csiro.au/projects/DDE/repos/pyimpuyte",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.6',
)

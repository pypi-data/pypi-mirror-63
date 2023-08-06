"""
setup.py: install python package
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_ms_sql", # Replace with your own username
    version="0.0.2",
    author="Timothy Reeder",
    author_email="timothy.reeder23@gmail.com",
    description="A small utility package that makes connecting to Microsoft SQL easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheBookReeder/py-ms-sql",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

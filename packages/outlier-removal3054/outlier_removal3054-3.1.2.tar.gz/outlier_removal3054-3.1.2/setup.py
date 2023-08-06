
from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="outlier_removal3054",
    version="3.1.2",
    description="A Python package for removing outliers in dataset using the Interquartile Range technique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Mehak garg",
    author_email="mehakgarg426@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["outliers"],
    include_package_data=True,
    install_requires=['pandas',
                      'numpy'
     ],
    entry_points={
        "console_scripts": [
            "remove-outlier = outliers.out:main",
        ]
    },
)
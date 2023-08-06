from setuptools import setup
import setuptools

setup(name='grooming',
version='0.2',
description='Grooming is a easiest way to clean-up the text',
author='Jayant Singh',
author_email='jayantsingh75@gmail.com',
url="https://github.com/jaysin60/grooming",
packages=setuptools.find_packages(),
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
python_requires='>=3.6',
install_requires = ['nltk','word2number']
)

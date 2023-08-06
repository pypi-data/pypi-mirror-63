#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.rst", "r") as fh:
	long_description = fh.read()
	
setuptools.setup(
	name="pycaptchagen",
	version="0.1.0",
	author="Christopher Hackmeyer",
	author_email="cbhackmeyer@allisforall.dedyn.io",
	description="Generate once-off \"CAPTCHA\"-type images and audio files from the command line.",
	long_description=long_description,
	long_description_content_type="text/x-rst",
	packages=setuptools.find_packages(),
	scripts=["bin/pycaptchagen"],
	license="The Unlicense (Public Domain)",
    data_files=[("", ["LICENSE"])],
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    install_requires=['captcha'],
    python_requires="~=3.2",
)

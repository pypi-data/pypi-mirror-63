#!/usr/bin/env python

# Copyright (c) 2009 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from setuptools import setup

setup(
    name="gyp-next",
    version="0.1",
    description="A fork of the GYP build system for use in the Node.js projects",
    author="Ujjwal Sharma",
    author_email="ryzokuken@disroot.org",
    url="https://github.com/nodejs/gyp-next",
    package_dir={"": "pylib"},
    packages=["gyp", "gyp.generator"],
    entry_points={"console_scripts": ["gyp=gyp:script_main"]},
)

#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains general tests for solstice-tools-snowgenerator
"""

import pytest

from solstice.tools.snowgenerator import __version__


def test_version():
    assert __version__.__version__

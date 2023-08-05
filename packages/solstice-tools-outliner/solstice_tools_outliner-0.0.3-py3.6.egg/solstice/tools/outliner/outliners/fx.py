#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains outliner implementations for Solstice FX assets
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

from artellapipe.tools.outliner.widgets import baseoutliner


class SoslticeFxOutilner(baseoutliner.BaseOutliner, object):
    def __init__(self, project, parent=None):
        super(SoslticeFxOutilner, self).__init__(project=project, parent=parent)

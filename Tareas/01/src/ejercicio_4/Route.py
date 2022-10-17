# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Route Class
"""
import sys


class Route(object):
    def __init__(self, name, value, realCost,iteration, node):
        self.name = name
        self.value = value
        self.iteration = iteration
        self.node = node
        self.realCost = realCost

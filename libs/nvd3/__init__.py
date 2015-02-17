#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Python-nvd3 is a Python wrapper for NVD3 graph library.
NVD3 is an attempt to build re-usable charts and chart components
for d3.js without taking away the power that d3.js gives you.

Project location : https://github.com/areski/python-nvd3
"""

<<<<<<< HEAD
__version__ = '0.13.5'
=======
__version__ = '0.12.2'  # edit also docs/source/conf.py
>>>>>>> b3c763ecf687c7317f4a0af05d07db99af008e81
__all__ = ['lineChart', 'pieChart', 'lineWithFocusChart',
           'stackedAreaChart', 'multiBarHorizontalChart',
           'linePlusBarChart', 'cumulativeLineChart',
           'scatterChart', 'discreteBarChart', 'multiBarChart',
           'linePlusBarWithFocusChart']


from .lineChart import lineChart
from .pieChart import pieChart
from .lineWithFocusChart import lineWithFocusChart
from .stackedAreaChart import stackedAreaChart
from .multiBarHorizontalChart import multiBarHorizontalChart
from .linePlusBarChart import linePlusBarChart
from .cumulativeLineChart import cumulativeLineChart
from .scatterChart import scatterChart
from .discreteBarChart import discreteBarChart
from .multiBarChart import multiBarChart
from .linePlusBarWithFocusChart import linePlusBarWithFocusChart
from . import ipynb

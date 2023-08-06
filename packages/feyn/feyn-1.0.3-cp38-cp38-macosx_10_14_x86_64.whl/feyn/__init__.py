"""
This is the SDK to build and execute Feyn-models.
"""
import pkg_resources  # part of setuptools
from ._dotrender import DotRenderer
from ._graph import Graph
from ._qgraph import QGraph
from ._qlattice import QLattice

from . import adapters

__all__ = ['DotRenderer', 'Graph', 'QGraph', 'QLattice', 'adapters']

__version__ = pkg_resources.require("feyn")[0].version 

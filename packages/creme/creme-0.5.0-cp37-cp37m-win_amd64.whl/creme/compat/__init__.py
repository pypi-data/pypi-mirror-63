"""Compatibility with other libraries.

This module contains adapters for making ``creme`` estimators compatible with other libraries, and
vice-versa whenever possible.

"""
from .pytorch import PyTorch2CremeRegressor
from .sklearn import convert_creme_to_sklearn
from .sklearn import convert_sklearn_to_creme
from .sklearn import SKL2CremeClassifier
from .sklearn import SKL2CremeRegressor
from .sklearn import Creme2SKLRegressor
from .sklearn import Creme2SKLClassifier
from .sklearn import Creme2SKLClusterer
from .sklearn import Creme2SKLTransformer


__all__ = [
    'convert_creme_to_sklearn',
    'convert_sklearn_to_creme',
    'Creme2SKLRegressor',
    'Creme2SKLClassifier',
    'Creme2SKLClusterer',
    'Creme2SKLTransformer',
    'PyTorch2CremeRegressor',
    'SKL2CremeClassifier',
    'SKL2CremeRegressor'
]

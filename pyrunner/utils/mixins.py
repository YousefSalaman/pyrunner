"""
Module for any mixin class or metaclass in the utilities module.
"""

from .type_abc import TypeABCMeta
from .cls_prop import CPEnabledMeta


class CPEnabledTypeABCMeta(CPEnabledMeta, TypeABCMeta):
    """
    A metaclass that mixes the functionality of using classproperties and type
    checking for ABCs.
    """


class CPEnabledTypeABC(object):
    """
    A helper class for CPEnabledTypeABCMeta that enables using classproperties
    and type checking for ABCs just by inhereting from this class directly.
    """

    __slots__ = ()
    __metaclass__ = CPEnabledTypeABCMeta

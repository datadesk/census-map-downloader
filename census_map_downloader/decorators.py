#! /usr/bin/env python
# -*- coding: utf-8 -*
"""
Decorators to help manage our custom classes.
"""
TABLE_LIST = []


def register(cls):
    """
    A decorator to register new table configuration classes.
    """
    TABLE_LIST.append(cls)
    return cls

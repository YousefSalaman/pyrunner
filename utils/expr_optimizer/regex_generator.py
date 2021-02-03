# -*- coding: utf-8 -*-
"""
This module helps create the regexes that will be used for decomposing
repeating terms found on the given set of equations. These regexes are
generated by counting the maximum nested parenthesis level of a given set of
equations.

The parentheses nesting level refers to the amount of parentheses pairs within
a syntactically correct expression. A generic mathematical expression normally
has an outer pair of parentheses, which is used to either encapsulate an
argument or an expression, and, within these, there are more parentheses pairs
doing the same thing.

    - For example, the expression "sin(3 + (23*x))" has a nested parenthesis
      level of 2 since it uses 2 pairs of parentheses to fully encapsulate its
      argument. The outer pair in this expression is the one used to
      encapsulate sin's argument; this is the 1st nested level.

The max nesting level is later used in conjunction with some basic regexes,
that match key parts of what a mathematical expression in Python can or must
contain when it's syntactically correct, to build two regexes that can match an
expression with the same nested parentheses level or lower.

The two regex expression built here are:

    - func_expr_regex: This is used to exactly match functions within the set
      of equations.

    - mult_expr_regex: This is used to match more generic expressions within
      the set of equations. Unlike the first regex, which will always match a
      function correctly, this mostly matches a term correctly. Some things
      throughout the code correct this to perform the adequate matching and
      decomposition.
"""

import re

# Atomic regexes for building more complex regexes

_FUNC = "[a-zA-Z0-9_]*"  # Will detect a function or multiplication
_UNFUNC = "(?<![a-zA-Z0-9_])"  # Lookbehind regex that prevents any function from being detected
_STRICT_FUNC = "[a-zA-Z0-9_]+"  # Strictly detects functions (excludes multiplication)
_NEG_SIGN = r'\-?'  # Negative sign
_TERM = r"\-?([a-zA-Z0-9_/\-\+\*\.]|\*\*[a-zA-Z0-9/\-\+\*\.]*)*"  # Generic math term


def generateMatchRegexes(calc_str):
    """
    Create regexes to decompose repeating terms on the given set of equations,
    and these are generated by counting the maximum nested parenthesis level of
    the expression string.
    """

    max_lvl = _find_max_nested_parenthesis_level(calc_str)

    return _build_general_expr_regexes(max_lvl)


def _pad_term(expr_str):
    """Create a expression with parenthesis padded with terms."""

    return r"\(" + _TERM + expr_str + _TERM + r"\)"


def _find_max_nested_parenthesis_level(calc_str):

    max_lvl = 0  # Current maximum nested parenthesis level
    lvl_cnt = 0  # Counter for current nested parenthesis level

    # Verify expression string for its max nested parenthesis level
    for char in calc_str:

        if char == "(":  # Increase the current level count by 1 for each "(" found
            lvl_cnt += 1
        elif char == ")":  # Decrease the current level count by 1 for each ")" found
            lvl_cnt -= 1

        if max_lvl < lvl_cnt:  # Update max level
            max_lvl = lvl_cnt

    return max_lvl


def _build_general_expr_regexes(max_lvl):

    # Initial regex expression
    base_expr_str = _NEG_SIGN + "(" + _FUNC + r"\(" + _TERM + r"\)" + "|" + _TERM + ")*"

    # Builds most of the regex by using the maximum level as a reference
    lvl_cnt = 0
    while lvl_cnt < max_lvl - 2:
        base_expr_str = _NEG_SIGN + "(" + _FUNC + _pad_term(base_expr_str) + "|" + base_expr_str + ")*"
        lvl_cnt += 1

    # Finish building regexes
    func_expr_regex = re.compile("(?P<gen_func>"+ _STRICT_FUNC + _pad_term(base_expr_str) + ")")
    mult_expr_regex = re.compile("(?P<gen_mult>" + _UNFUNC + _pad_term(base_expr_str) + "|" + _TERM + ")")

    return func_expr_regex, mult_expr_regex

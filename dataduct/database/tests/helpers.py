"""Helpers for Database Tests
"""
from __future__ import absolute_import
from nose.tools import eq_

from ..table import Table
from ..view import View
from ..sql import SqlScript
from six.moves import zip


def create_table(sql):
    """Creates a table object from a SQL string
    """
    return Table(SqlScript(sql))


def create_view(sql):
    """Creates a view object from a SQL string
    """
    return View(SqlScript(sql))


def compare_scripts(actual_script, expected_script):
    """Validates a SqlScript chain
    """
    assert len(actual_script) == len(expected_script)
    for actual, expected in zip(actual_script, expected_script):
        eq_(actual.sql(), expected)

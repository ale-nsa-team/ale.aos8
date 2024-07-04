# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


"""
The arg spec for the aos8_command module
"""


class CommandArgs(object):  # pylint: disable=R0903
    """The arg spec for the aos8_command module
    """

    argument_spec = {
        "commands": {"required": True, "type": "list", "elements": "raw"},
        "output": {"aliases": ["output"], "type": "list", "elements": "str"},
    }  # pylint: disable=C0301

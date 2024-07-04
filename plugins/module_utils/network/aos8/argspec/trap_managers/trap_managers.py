# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The arg spec for the aos8_trap_managers module
"""

class Trap_managersArgs(object):  # pylint: disable=R0903
    """The arg spec for the aos8_trap_managers module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "host": {"type": "str", "required": True},
                "port": {"type": "int", "required": False, "default": 161},
                "version": {
                    "type": "str", 
                    "required": False, 
                    "choices": [
                        "v1",
                        "v2",
                        "v3"
                    ],
                    "default": "v2"
                },
                "string": {"type": "str", "required": False, "default": "public"},
                "state": {"type": "str", "required": False, "default": "enable"},
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "rendered",
                "gathered",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
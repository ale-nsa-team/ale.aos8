# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
                "port": {"type": "int", "default": 162},
                "string": {"type": "str", "default": "public"},
                "version": {"type": "str", "choices": ["v1", "v2", "v3"], "default": "v2"},
                "state": {"type": "str", "choices": ["enable", "disable"], "default": "enable"},
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
            "choices": ["merged", "replaced", "overridden", "deleted", "gathered", "rendered", "parsed"],
            "default": "merged",
        },
    }

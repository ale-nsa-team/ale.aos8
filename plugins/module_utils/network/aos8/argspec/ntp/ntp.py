# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the aos8_ntp module
"""


class Ntp_Args(object):  # pylint: disable=R0903
    """The arg spec for the aos8_ntp module"""

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "servers": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "server": {"type": "str", "required": True},
                        "minpoll": {"type": "int"},
                        "maxpoll": {"type": "int"},
                        "version": {"type": "int", "choices": [1, 2, 3, 4]},
                        "prefer": {"type": "bool"},
                        "burst": {"type": "bool"},
                        "iburst": {"type": "bool"},
                    },
                },
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
            "choices": ["merged", "replaced", "overridden", "deleted", "gathered", "rendered", "parsed"],
            "default": "merged",
        },
    }

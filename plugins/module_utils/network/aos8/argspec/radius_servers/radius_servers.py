# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the aos8_radius_servers module
"""


class Radius_serversArgs(object):  # pylint: disable=R0903
    """The arg spec for the aos8_radius_servers module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {"type": "str", "required": True},
                "host": {"type": "str"},
                "key": {"type": "str", "no_log": True},
                "auth_port": {"type": "int", "default": 1812},
                "acct_port": {"type": "int", "default": 1813},
                "retransmit": {"type": "int", "default": 3},
                "timeout": {"type": "int", "default": 2},
                "vrf": {"type": "str", "default": "default"},
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
            "choices": ["merged", "replaced", "overridden", "deleted", "gathered", "rendered", "parsed"],
            "default": "merged",
        },
    }

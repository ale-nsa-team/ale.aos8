# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the aos8_vlans module
"""


class VlansArgs(object):  # pylint: disable=R0903
    """The arg spec for the aos8_vlans module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "vlan_id": {"type": "int", "required": True},
                "name": {"type": "str"},
                "admin": {"type": "str", "choices": ["enable", "disable"]},
                "mtu": {"type": "int"},
                "operational_state": {"type": "str", "choices": ["enable", "disable"]},
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
            "choices": ["merged", "replaced", "overridden", "deleted", "gathered", "rendered", "parsed"],
            "default": "merged",
        },
    }

#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The arg spec for the ios_vlans module
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


class VlansArgs(object):
    """The arg spec for the aos8_vlans module"""

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {"type": "str"},
                "vlan_id": {"required": True, "type": "int"},
                "mtu": {"type": "int", "default" : 1500},
                "admin": {"type": "str", "choices": ["enable", "disable"], "default": "enable"},
                "operational_state": {"type": "str", "choices": ["enable", "disable"]},
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
                "parsed",
                "gathered",
            ],
            "default": "merged",
            "type": "str",
        },
    }
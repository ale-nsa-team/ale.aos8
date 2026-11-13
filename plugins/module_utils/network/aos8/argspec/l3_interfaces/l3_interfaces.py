# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the aos8_l3_interfaces module
"""


class L3_interfacesArgs(object):  # pylint: disable=R0903
    """The arg spec for the aos8_l3_interfaces module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {"type": "str", "required": True},
                "address": {"type": "str"},
                "mask": {"type": "str"},
                "type": {"type": "str", "choices": ["vlan"]},
                "port_id": {"type": "str"},
                "vrf": {"type": "str"},
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
            "choices": ["merged", "replaced", "overridden", "deleted", "gathered", "rendered", "parsed"],
            "default": "merged",
        },
    }

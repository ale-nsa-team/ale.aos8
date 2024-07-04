# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
                "vrf": {"type": "str", "required": False},
                "name": {"type": "str", "required": True},
                "address": {"type": "str", "required": True},
                "mask": {"type": "str", "required": False},
                "type": {
                    "type": "str",
                    "required" : False,
                    "choices": [
                        "vlan",
                        "rtr-port",
                        "tunnel",
                    ],
                },
                "port_id": {"type": "str", "required": False},
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
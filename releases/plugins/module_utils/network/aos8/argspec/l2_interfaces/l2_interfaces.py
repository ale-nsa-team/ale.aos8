# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The arg spec for the aos8_l2_interfaces module
"""

class L2_interfacesArgs(object):  # pylint: disable=R0903
    """The arg spec for the aos8_l2_interfaces module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "vlan_id": {"type": "int", "required": True},
                "port_type": {
                    "type": "str",
                    "required" : True,
                    "choices": [
                        "port",
                        "linkagg",
                    ],
                },
                "port_number": {"type": "str", "required": True},
                "mode": {
                    "type": "str",
                    "required" : True,
                    "choices": [
                        "untagged",
                        "tagged",
                    ],
                },
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
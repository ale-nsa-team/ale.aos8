# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the aos8_static_routes module
"""


class Static_routesArgs(object):  # pylint: disable=R0903
    """The arg spec for the aos8_static_routes module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "routes": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "dest": {"type": "str", "required": True},
                        "next_hops": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "forward_router_address": {"type": "str"},
                                "interface": {"type": "str"},
                                "admin_distance": {"type": "int"},
                                "tag": {"type": "int"},
                                "description": {"type": "str"},
                            },
                        },
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

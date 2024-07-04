#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################
"""
The arg spec for the eos_static_routes module
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


class Static_routesArgs(object):
    """The arg spec for the aos8_static_routes module"""

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "elements": "dict",
            "options": {
                "address_families": {
                    "elements": "dict",
                    "options": {
                        "afi": {
                            "choices": ["ipv4", "ipv6"],
                            "required": True,
                            "type": "str",
                        },
                        "routes": {
                            "elements": "dict",
                            "options": {
                                "dest": {"required": True, "type": "str"},
                                "next_hops": {
                                    "elements": "dict",
                                    "options": {
                                        "admin_distance": {"type": "int"},
                                        "description": {"type": "str"},
                                        "forward_router_address": {
                                            "type": "str",
                                        },
                                        "interface": {"type": "str"},
                                        "nexthop_grp": {"type": "str"},
                                        "mpls_label": {"type": "int"},
                                        "tag": {"type": "int"},
                                        "track": {"type": "str"},
                                        "vrf": {"type": "str"},
                                    },
                                    "type": "list",
                                },
                            },
                            "type": "list",
                        },
                    },
                    "type": "list",
                },
                "vrf": {"type": "str"},
            },
            "type": "list",
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "deleted",
                "merged",
                "overridden",
                "replaced",
                "gathered",
                "rendered",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
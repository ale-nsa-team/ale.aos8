# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The arg spec for the aos8_bgp module
"""

class Bgp_Args(object):  # pylint: disable=R0903
    """The arg spec for the aos8_bgp module"""

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "running_config": {"type": "str"},
        "state": {
            "default": "merged",
            "type": "str",
            "choices": [
                "deleted",
                "purged",
                "merged",
                "replaced",
                "overridden",
                "gathered",
                "rendered",
                "parsed",
            ],
        },
        "config": {
            "type": "dict",
            "options": {
                "as_number": {"type": "str"},
                "bgp_admin_state": {"type": "str", "choices": ["enable", "disable"]},
                "neighbor": {
                    "elements": "dict",
                    "type": "list",
                    "options": {
                        "neighbor_address": {"type": "str", "aliases": ["peer"]},
                        "remote_as": {"type": "str"},
                        "neighbor_admin_state": {"type": "str", "choices": ["enable", "disable"]},
                    },
                },
            },
        },
    }  # pylint: disable=C0301

# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the aos8_bgp module
"""


class Bgp_Args(object):  # pylint: disable=R0903
    """The arg spec for the aos8_bgp module"""

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "as_number": {"type": "str"},
                "bgp_admin_state": {"type": "str", "choices": ["enable", "disable"]},
                "neighbor": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "neighbor_address": {"type": "str", "required": True, "aliases": ["peer"]},
                        "remote_as": {"type": "str"},
                        "neighbor_admin_state": {"type": "str", "choices": ["enable", "disable"]},
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

# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the aos8_ospfv2 module
"""


class OspfV2_Args(object):  # pylint: disable=R0903
    """The arg spec for the aos8_ospfv2 module"""

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "admin_state": {"type": "str", "choices": ["enable", "disable"]},
                "areas": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "area_id": {"type": "str", "required": True},
                        "interfaces": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "interface": {"type": "str", "required": True},
                                "admin_state": {"type": "str", "choices": ["enable", "disable"]},
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

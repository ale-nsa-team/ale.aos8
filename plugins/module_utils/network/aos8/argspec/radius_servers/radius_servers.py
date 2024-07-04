# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The arg spec for the aos8_radius_servers module
"""

class Radius_serversArgs(object):  # pylint: disable=R0903
    """The arg spec for the aos8_radius_servers module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {"type": "str", "required": True},
                "host": {"type": "str", "required": True},
                "key": {"type": "str", "required": False},
                "auth_port": {"type": "int", "required": False, "default": 1812},
                "acct_port": {"type": "int", "required": False, "default": 1813},
                "retransmit": {"type": "int", "required": False, "default": 3},
                "timeout": {"type": "int", "required": False, "default": 2},
                "vrf": {"type": "str", "required": False, "default": "default"},
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
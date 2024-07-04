# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The arg spec for the aos8_switch_security module
"""

class Switch_securityArgs(object):  # pylint: disable=R0903
    """The arg spec for the aos8_switch_security module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "access_method": {
                    "type": "str", 
                    "required": True, 
                    "choices": [
                        "default",
                        "console",
                        "telnet",
                        "ssh",
                        "snmp",
                        "http",
                        "ftp",
                    ],
                },
                "aaa_servers_name": {"type": "str", "required": True},
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
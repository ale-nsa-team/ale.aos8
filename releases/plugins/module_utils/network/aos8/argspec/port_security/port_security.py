# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The arg spec for the aos8_port_security module
"""

class Port_securityArgs(object):  # pylint: disable=R0903
    """The arg spec for the aos8_port_security module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options":{
                "learning-window": {"type": "int", "required": False},
                "chassis": {
                    "type": "dict", 
                    "required": False,
                    "options":{         
                        "state": {
                            "type": "str",
                            "required" : False,
                            "choices": [
                                "locked",
                                "enable",
                                "disable",
                            ],
                        },                                       
                        "convert-to-static": {
                            "type": "str",
                            "required" : False,
                            "choices": [
                                "enable",
                                "disable",
                            ],
                        }, 
                    }
                },
                "port" : {
                    "type" : "list",
                    "elements": "dict",
                    "options": {
                        "port_number": {"type": "str", "required": True},
                        "mac": {
                            "type": "dict", 
                            "required": False,
                            "options" : {
                                "address": {"type": "str", "required": True},
                                "vlan": {"type": "int", "required": True},
                            }                            
                        },
                        "mac-range": { 
                            "type": "dict", 
                            "required": False,
                            "options" : {
                                "low": {"type": "str", "required": True},
                                "high": {"type": "str", "required": True},
                            }
                        },
                        "maximum": {"type": "int", "required": False},
                        "max-filtering": {"type": "int", "required": False},
                        "learn-trap-threshold": {"type": "int", "required": False},
                        "violation": {
                            "type": "str",
                            "required" : False,
                            "choices": [
                                "shutdown",
                                "restrict",
                                "discard",
                            ],
                        },    
                        "state": {
                            "type": "str",
                            "required" : False,
                            "choices": [
                                "locked",
                                "enable",
                                "disable",
                            ],
                        },     
                        "convert-to-static": {
                            "type": "str",
                            "required" : False,
                            "choices": [
                                "enable",
                                "disable",
                            ],
                        },                                            
                    },
                }
            }
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
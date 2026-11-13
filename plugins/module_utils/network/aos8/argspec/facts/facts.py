# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the aos8_facts module
"""


class FactsArgs(object):  # pylint: disable=R0903
    """The arg spec for the aos8_facts module"""

    choices = [
        "all",
        "bgp",
        "hostname",
        "l2_interfaces",
        "l3_interfaces",
        "ntp",
        "ospfv2",
        "radius_servers",
        "static_routes",
        "switch_security",
        "trap_managers",
        "vlans",
    ]

    argument_spec = {
        "gather_subset": {"type": "list", "elements": "str", "default": ["min"]},
        "gather_network_resources": {"type": "list", "elements": "str", "choices": choices},
    }

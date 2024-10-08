# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The arg spec for the aos8 facts module.
"""


class FactsArgs(object):  # pylint: disable=R0903
    """ The arg spec for the aos8_facts module
    """

    def __init__(self, **kwargs):
        pass

    choices = [
        'all',
        'l2_interfaces',
        'l3_interfaces',
        'radius_servers',
        'switch_security',
        'port_security',
        'trap_managers',
        'hostname',
        'vlans',
    ]

    argument_spec = {
        'gather_subset': dict(default=['!config'], type='list'),
        'gather_network_resources': dict(choices=choices,
                                         type='list'),
    }

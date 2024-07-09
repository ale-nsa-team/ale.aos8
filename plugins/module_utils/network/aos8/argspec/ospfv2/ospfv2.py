# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING ou https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The aos8 OSPFV2 argspec class
It is in this file the arguments for the OSPF module are defined.
"""

from __future__ import absolute_import, division, print_function

class OspfV2_Args(object):
    """
    The aos8 OSPFV2 argspec class
    """
    def __init__(self, **kwargs):
        pass
        
    argument_spec = {
        'config': {
            'type': 'dict',
            'options': {
                'admin_state': {'type': 'str', 'choices': ['enable', 'disable']},
                'areas': {
                    'type': 'list',
                    'elements': 'dict',
                    'options': {
                        'area_id': {'type': 'str', 'required': True},
                        'interfaces': {
                            'type': 'list',
                            'elements': 'dict',
                            'options': {
                                'interface': {'type': 'str', 'required': True},
                                'admin_state': {'type': 'str', 'choices': ['enable', 'disable']},
                                'area': {'type': 'str'}
                            }
                        }
                    }
                }
            }
        },
        'state': {'type': 'str', 'choices': ['merged', 'replaced', 'overridden', 'rendered', 'parsed'], 'default': 'merged'}
    }


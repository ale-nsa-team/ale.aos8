# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import NetworkTemplate

# Fonction pour générer la commande de configuration du système autonome BGP
def _tmplt_bgp_autonomous_system(config_data):
    command = "ip bgp autonomous-system {as_number}".format(**config_data)
    return command

# Fonction pour générer la commande de configuration d'un voisin BGP
def _tmplt_bgp_neighbor(config_data):
    command = "ip bgp neighbor {neighbor_address}".format(**config_data)
    if config_data.get("neighbor_remote_as"):
        command += " remote-as {neighbor_remote_as}".format(**config_data)
    if config_data.get("neighbor_admin_state"):
        command += " admin-state {neighbor_admin_state}".format(**config_data)
    return command

# Fonction pour générer la commande de configuration de l'état administratif BGP
def _tmplt_bgp_admin_state(config_data):
    command = "ip bgp admin-state {admin_state}".format(**config_data)
    return command

# Fonction pour générer la commande de débogage BGP
def _tmplt_debug_bgp(config_data):
    command = "debug ip bgp adv-loopback0 {state}".format(**config_data)
    return command

class Bgp_Template(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Bgp_Template, self).__init__(
            lines=lines,
            tmplt=self,
            module=module,
        )

    # Définition des parsers pour chaque type de commande
    PARSERS = [
        {
            "name": "bgp_autonomous_system",
            "getval": re.compile(
                r"""
                ip\sbgp\sautonomous-system\s
                (?P<as_num>\S+)
                """,
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_autonomous_system,
            "compval": "as_number",
            "result": {"as_number": "{{ as_num }}"},
        },
        {
            "name": "neighbor_address",
            "getval": re.compile(
                r"""
                ip\sbgp\sneighbor\s
                (?P<neighbor_address>\S+)
                """,
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_neighbor,
            "compval": "neighbor_address",
            "result": {
                "neighbor_address": "{{ neighbor_address }}",
            },
        },
        {
            "name": "neighbor_remote_as",
            "getval": re.compile(
                r"""
                ip\sbgp\sneighbor\s
                (?P<neighbor_address>\S+)
                \sremote-as\s
                (?P<remote_as>\S+)
                """,
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_neighbor,
            "compval": "neighbor_remote_as",
            "result": {
                "neighbor_address": "{{ neighbor_address }}",
                "neighbor_remote_as": "{{ remote_as }}",
            },
        },
        {
            "name": "neighbor_admin_state",
            "getval": re.compile(
                r"""
                ip\sbgp\sneighbor\s
                (?P<neighbor_address>\S+)
                \sadmin-state\s
                (?P<admin_state>\S+)
                """,
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_neighbor,
            "compval": "neighbor_admin_state",
            "result": {
                "neighbor_address": "{{ neighbor_address }}",
                "neighbor_admin_state": "{{ admin_state }}",
            },
        },
        {
            "name": "bgp_admin_state",
            "getval": re.compile(
                r"""
                ip\sbgp\sadmin-state\s
                (?P<admin_state>\S+)
                """,
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_admin_state,
            "compval": "admin_state",
            "result": {
                "admin_state": "{{ admin_state }}",
            },
        },
        {
            "name": "debug_bgp",
            "getval": re.compile(
                r"""
                debug\sip\sbgp\sadv-loopback0\s
                (?P<state>\S+)
                """,
                re.VERBOSE,
            ),
            "setval": _tmplt_debug_bgp,
            "compval": "state",
            "result": {
                "state": "{{ state }}",
            },
        },
    ]

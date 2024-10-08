# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The facts class for aos8
this file validates each subset of facts and selectively
calls the appropriate facts gathering function
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts import (
    FactsBase,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.hostname.hostname import HostnameFacts
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.vlans.vlans import VlansFacts
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.l2_interfaces.l2_interfaces import L2_interfacesFacts
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.l3_interfaces.l3_interfaces import L3_interfacesFacts
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.radius_servers.radius_servers import Radius_serversFacts
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.trap_managers.trap_managers import Trap_managersFacts
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.switch_security.switch_security import Switch_securityFacts
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.port_security.port_security import Port_securityFacts
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.ntp.ntp import Ntp_Facts
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.static_routes.static_routes import Static_routesFacts
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.ospfv2.ospfv2 import OspfV2_Facts
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.bgp.bgp import Bgp_Facts

FACT_LEGACY_SUBSETS = {}
FACT_RESOURCE_SUBSETS = dict(
    l2_interfaces=L2_interfacesFacts,
    l3_interfaces=L3_interfacesFacts,
    hostname=HostnameFacts,
    radius_servers=Radius_serversFacts,
    trap_managers=Trap_managersFacts,
    switch_security=Switch_securityFacts,
    port_security=Port_securityFacts,
    vlans=VlansFacts,
    ntp=Ntp_Facts,
    static_routes=Static_routesFacts,
    ospfv2=OspfV2_Facts,
    bgp=Bgp_Facts,
)


class Facts(FactsBase):
    """ The fact class for aos8
    """

    VALID_LEGACY_GATHER_SUBSETS = frozenset(FACT_LEGACY_SUBSETS.keys())
    VALID_RESOURCE_SUBSETS = frozenset(FACT_RESOURCE_SUBSETS.keys())

    def __init__(self, module):
        super(Facts, self).__init__(module)

    def get_facts(self, legacy_facts_type=None, resource_facts_type=None, data=None):
        """ Collect the facts for aos8

        :param legacy_facts_type: List of legacy facts types
        :param resource_facts_type: List of resource fact types
        :param data: previously collected conf
        :rtype: dict
        :return: the facts gathered
        """
        if self.VALID_RESOURCE_SUBSETS:
            self.get_network_resources_facts(FACT_RESOURCE_SUBSETS, resource_facts_type, data)

        if self.VALID_LEGACY_GATHER_SUBSETS:
            self.get_network_legacy_facts(FACT_LEGACY_SUBSETS, legacy_facts_type)

        return self.ansible_facts, self._warnings

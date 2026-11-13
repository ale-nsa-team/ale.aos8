# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type


from unittest.mock import MagicMock, patch

from ansible_collections.ale.aos8.plugins.modules import aos8_facts
from ansible_collections.ale.aos8.tests.unit.modules.utils import set_module_args

from .aos8_module import TestAos8Module, load_fixture


FIXTURES = {
    "show vlan": "aos8_vlans.txt",
    "show vlan members": "aos8_l2_interfaces.txt",
    'show configuration snapshot | grep "ip interface"': "aos8_l3_interfaces.txt",
    "show configuration snapshot | grep '^system name'": "aos8_hostname.txt",
    'show configuration snapshot | grep "aaa radius-server"': "aos8_radius_servers.txt",
    'show configuration snapshot | grep "snmp station"': "aos8_trap_managers.txt",
    'show configuration snapshot | grep "aaa authentication"': "aos8_switch_security.txt",
    "show configuration snapshot ip-routing": "aos8_static_routes.txt",
    "show configuration snapshot ospf": "aos8_ospfv2.txt",
    "show configuration snapshot bgp": "aos8_bgp.txt",
    "show configuration snapshot ntp": "aos8_ntp.txt",
}
RESOURCES = sorted(
    ["bgp", "hostname", "l2_interfaces", "l3_interfaces", "ntp", "ospfv2", "radius_servers"]
    + ["static_routes", "switch_security", "trap_managers", "vlans"],
)


class TestAos8FactsModule(TestAos8Module):
    module = aos8_facts

    def setUp(self):
        super(TestAos8FactsModule, self).setUp()
        self.connection = MagicMock()
        self.connection.get.side_effect = lambda command: load_fixture(FIXTURES[command])
        self._patches = [
            patch(
                "ansible_collections.ansible.netcommon.plugins.module_utils.network.common."
                "facts.facts.get_resource_connection",
                return_value=self.connection,
            ),
            patch(
                "ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.legacy.base.run_commands",
                side_effect=lambda module, commands: [load_fixture("aos8_show_system.txt")],
            ),
        ]
        for item in self._patches:
            item.start()

    def tearDown(self):
        super(TestAos8FactsModule, self).tearDown()
        for item in self._patches:
            item.stop()

    def facts(self, **args):
        set_module_args(args)
        return self.execute_module()["ansible_facts"]

    def test_default_collects_basic_facts_only(self):
        facts = self.facts()
        self.assertEqual(facts["ansible_net_model"], "OS687024-SIM")
        self.assertEqual(facts["ansible_net_version"], "8.11.162.R01")
        self.assertEqual(facts["ansible_net_hostname"], "val-os1")
        self.assertEqual(facts["ansible_net_network_os"], "aos8")
        self.assertEqual(
            facts["ansible_net_system"],
            "Alcatel-Lucent Enterprise OS687024-SIM 8.11.162.R01 GA, August 19, 2026.",
        )
        self.assertEqual(facts["ansible_network_resources"], {})

    def test_no_basic_facts(self):
        facts = self.facts(gather_subset=["!all", "!min"], gather_network_resources=["hostname"])
        self.assertNotIn("ansible_net_version", facts)
        self.assertEqual(facts["ansible_network_resources"], {"hostname": {"hostname": "val-os1"}})

    def test_all_resources(self):
        facts = self.facts(gather_subset=["all"], gather_network_resources=["all"])
        self.assertEqual(sorted(facts["ansible_network_resources"]), RESOURCES)
        self.assertEqual(facts["ansible_net_version"], "8.11.162.R01")
        self.assertEqual(len(facts["ansible_network_resources"]["vlans"]), 4)
        self.assertEqual(facts["ansible_network_resources"]["bgp"]["as_number"], "65001")

    def test_each_resource_alone(self):
        for resource in RESOURCES:
            facts = self.facts(gather_subset=["!all", "!min"], gather_network_resources=[resource])
            self.assertEqual(list(facts["ansible_network_resources"]), [resource])
            self.assertTrue(facts["ansible_network_resources"][resource], resource)

    def test_unknown_resource_fails(self):
        set_module_args(dict(gather_network_resources=["port_security"]))
        self.execute_module(failed=True)

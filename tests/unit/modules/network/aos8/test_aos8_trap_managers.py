# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ale.aos8.plugins.modules import aos8_trap_managers

from .aos8_module import TestAos8ResourceModule


class TestAos8TrapManagersModule(TestAos8ResourceModule):
    module = aos8_trap_managers
    fixture = "aos8_trap_managers.txt"

    def test_gathered(self):
        result = self.run_module(state="gathered")
        self.assertEqual(
            result["gathered"],
            [
                {"host": "192.168.121.250", "port": 162, "string": "valtest", "version": "v2", "state": "enable"},
                {"host": "192.168.121.249", "port": 162, "string": "valtest", "version": "v1", "state": "disable"},
            ],
        )

    def test_merged_new_with_defaults(self):
        self.run_module(
            changed=True,
            config=[dict(host="10.0.0.9")],
            commands=['snmp station 10.0.0.9 162 "public" v2 enable'],
        )

    def test_merged_idempotent(self):
        self.run_module(config=[dict(host="192.168.121.250", string="valtest")], commands=[])

    def test_merged_change(self):
        self.run_module(
            changed=True,
            config=[dict(host="192.168.121.249", string="valtest", version="v1", state="enable")],
            commands=['snmp station 192.168.121.249 162 "valtest" v1 enable'],
        )

    def test_deleted(self):
        self.run_module(
            changed=True,
            state="deleted",
            config=[dict(host="192.168.121.250")],
            commands=["no snmp station 192.168.121.250"],
        )

    def test_deleted_all(self):
        self.run_module(
            changed=True,
            state="deleted",
            commands=["no snmp station 192.168.121.250", "no snmp station 192.168.121.249"],
            sort=True,
        )

    def test_overridden(self):
        self.run_module(
            changed=True,
            state="overridden",
            config=[dict(host="192.168.121.250", string="valtest")],
            commands=["no snmp station 192.168.121.249"],
        )

    def test_rendered(self):
        result = self.run_module(state="rendered", config=[dict(host="10.0.0.9", port=1162, string="ops", version="v3")])
        self.assertEqual(result["rendered"], ['snmp station 10.0.0.9 1162 "ops" v3 enable'])

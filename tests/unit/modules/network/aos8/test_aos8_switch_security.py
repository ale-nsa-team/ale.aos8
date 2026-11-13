# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ale.aos8.plugins.modules import aos8_switch_security

from .aos8_module import TestAos8ResourceModule


class TestAos8SwitchSecurityModule(TestAos8ResourceModule):
    module = aos8_switch_security
    fixture = "aos8_switch_security.txt"

    def test_gathered(self):
        result = self.run_module(state="gathered")
        self.assertEqual(
            result["gathered"],
            [
                {"access_method": "default", "aaa_servers_name": "local"},
                {"access_method": "console", "aaa_servers_name": "local"},
                {"access_method": "telnet", "aaa_servers_name": "local"},
                {"access_method": "ftp", "aaa_servers_name": "local"},
                {"access_method": "ssh", "aaa_servers_name": "local"},
            ],
        )

    def test_merged_new(self):
        self.run_module(
            changed=True,
            config=[dict(access_method="http", aaa_servers_name="local")],
            commands=['aaa authentication http "local"'],
        )

    def test_merged_idempotent(self):
        self.run_module(config=[dict(access_method="telnet", aaa_servers_name="local")], commands=[])

    def test_merged_change(self):
        self.run_module(
            changed=True,
            config=[dict(access_method="ssh", aaa_servers_name="val-radius")],
            commands=['aaa authentication ssh "val-radius"'],
        )

    def test_merged_without_server_fails(self):
        self.run_module(failed=True, config=[dict(access_method="http")])

    def test_deleted(self):
        self.run_module(
            changed=True,
            state="deleted",
            config=[dict(access_method="ftp")],
            commands=["aaa authentication ftp default"],
        )

    def test_deleted_never_resets_default(self):
        self.run_module(state="deleted", config=[dict(access_method="default")], commands=[])

    def test_rendered(self):
        result = self.run_module(state="rendered", config=[dict(access_method="snmp", aaa_servers_name="local")])
        self.assertEqual(result["rendered"], ['aaa authentication snmp "local"'])

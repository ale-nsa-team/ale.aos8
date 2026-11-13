# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ale.aos8.plugins.modules import aos8_hostname

from .aos8_module import TestAos8ResourceModule


class TestAos8HostnameModule(TestAos8ResourceModule):
    module = aos8_hostname
    fixture = "aos8_hostname.txt"

    def test_gathered(self):
        result = self.run_module(state="gathered")
        self.assertEqual(result["gathered"], {"hostname": "val-os1"})

    def test_parsed(self):
        result = self.run_module(state="parsed", running_config='system name "core-1"')
        self.assertEqual(result["parsed"], {"hostname": "core-1"})

    def test_merged(self):
        self.run_module(changed=True, config=dict(hostname="core-1"), commands=['system name "core-1"'])

    def test_merged_idempotent(self):
        self.run_module(config=dict(hostname="val-os1"), commands=[])

    def test_replaced(self):
        self.run_module(
            changed=True,
            state="replaced",
            config=dict(hostname="core-1"),
            commands=['system name "core-1"'],
        )

    def test_overridden_idempotent(self):
        self.run_module(state="overridden", config=dict(hostname="val-os1"), commands=[])

    def test_rendered(self):
        result = self.run_module(state="rendered", config=dict(hostname="core-1"))
        self.assertEqual(result["rendered"], ['system name "core-1"'])

    def test_deleted_is_not_supported(self):
        self.run_module(failed=True, state="deleted")

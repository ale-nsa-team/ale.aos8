# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type


from unittest.mock import patch

from ansible_collections.ale.aos8.plugins.modules import aos8_command
from ansible_collections.ale.aos8.tests.unit.modules.utils import set_module_args

from .aos8_module import TestAos8Module, load_fixture


class TestAos8CommandModule(TestAos8Module):
    module = aos8_command

    def setUp(self):
        super(TestAos8CommandModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.ale.aos8.plugins.modules.aos8_command.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()
        self.run_commands.side_effect = lambda module, commands: [
            load_fixture("aos8_show_system.txt") for item in commands
        ]
        self.mock_warn = patch("ansible.module_utils.basic.AnsibleModule.warn")
        self.warn = self.mock_warn.start()

    def tearDown(self):
        super(TestAos8CommandModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_warn.stop()

    def sent(self):
        return [item["command"] for item in self.run_commands.call_args[0][1]]

    def test_single_command(self):
        set_module_args(dict(commands=["show system"]))
        result = self.execute_module()
        self.assertEqual(len(result["stdout"]), 1)
        self.assertIn("OS687024-SIM 8.11.162.R01", result["stdout"][0])
        self.assertEqual(result["stdout_lines"][0][0], "System:")
        self.assertEqual(self.sent(), ["show system"])

    def test_multiple_commands(self):
        set_module_args(dict(commands=["show system", "show vlan"]))
        result = self.execute_module()
        self.assertEqual(len(result["stdout"]), 2)
        self.assertEqual(self.sent(), ["show system", "show vlan"])

    def test_command_with_prompt(self):
        set_module_args(dict(commands=[dict(command="no vlan 40", prompt="[Yy]/[Nn]", answer="y")]))
        self.execute_module()
        sent = self.run_commands.call_args[0][1][0]
        self.assertEqual(sent["command"], "no vlan 40")
        self.assertEqual(sent["prompt"], "[Yy]/[Nn]")
        self.assertEqual(sent["answer"], "y")

    def test_check_mode_only_sends_show_commands(self):
        set_module_args(dict(commands=["show vlan", "vlan 41 admin-state enable"], _ansible_check_mode=True))
        result = self.execute_module()
        self.assertEqual(self.sent(), ["show vlan"])
        self.assertEqual(len(result["stdout"]), 1)
        self.warn.assert_called_once()

    def test_commands_are_required(self):
        set_module_args(dict())
        self.execute_module(failed=True)

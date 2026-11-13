# (c) 2016 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import json
import os

from ansible_collections.ale.aos8.tests.unit.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
)


fixture_path = os.path.join(os.path.dirname(__file__), "fixtures")
fixture_data = {}


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()
    try:
        data = json.loads(data)
    except Exception:
        pass

    fixture_data[path] = data
    return data


class TestAos8Module(ModuleTestCase):
    def execute_module(
        self,
        failed=False,
        changed=False,
        commands=None,
        inputs=None,
        sort=True,
        defaults=False,
        transport="cli",
        filename=None,
    ):
        if filename is None:
            self.load_fixtures(commands, transport=transport)
        else:
            self.load_fixtures(
                commands,
                transport=transport,
                filename=filename,
            )

        if failed:
            result = self.failed()
            self.assertTrue(result["failed"], result)
        else:
            result = self.changed(changed)
            self.assertEqual(result["changed"], changed, result)
        if commands is not None:
            if transport == "eapi":
                cmd = []
                value = []
                for item in result["commands"]:
                    cmd.append(item["cmd"])
                    if "input" in item:
                        value.append(item["input"])
                if sort:
                    self.assertEqual(sorted(commands), sorted(cmd), cmd)
                else:
                    self.assertEqual(commands, cmd, cmd)
                if inputs:
                    self.assertEqual(inputs, value, value)
            else:
                if sort:
                    self.assertEqual(
                        sorted(commands),
                        sorted(result["commands"]),
                        result["commands"],
                    )
                else:
                    self.assertEqual(
                        commands,
                        result["commands"],
                        result["commands"],
                    )

        return result

    def failed(self):
        with self.assertRaises(AnsibleFailJson) as exc:
            self.module.main()

        result = exc.exception.args[0]
        self.assertTrue(result["failed"], result)
        return result

    def changed(self, changed=False):
        with self.assertRaises(AnsibleExitJson) as exc:
            self.module.main()

        result = exc.exception.args[0]
        self.assertEqual(result["changed"], changed, result)
        return result

    def load_fixtures(self, commands=None, transport="cli", filename=None):
        pass


class TestAos8ResourceModule(TestAos8Module):
    """Base class for the resource module tests.

    The device is replaced by a fixture holding the real output of the command
    the facts class reads, captured from an OmniSwitch running AOS 8.11.
    """

    fixture = None

    def setUp(self):
        super(TestAos8ResourceModule, self).setUp()
        from unittest.mock import MagicMock, patch

        base = "ansible_collections.ansible.netcommon.plugins.module_utils.network.common."
        self.connection = MagicMock()
        self._patches = [
            patch(base + "cfg.base.get_resource_connection", return_value=self.connection),
            patch(base + "facts.facts.get_resource_connection", return_value=self.connection),
            patch(
                "ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.base."
                "Aos8FactsBase.get_device_data",
                side_effect=self._device_data,
            ),
        ]
        for item in self._patches:
            item.start()
        self._data = load_fixture(self.fixture)

    def tearDown(self):
        super(TestAos8ResourceModule, self).tearDown()
        for item in self._patches:
            item.stop()

    def hide_secrets(self, commands):
        return commands

    def _device_data(self, *args, **kwargs):
        return self._data

    def run_module(self, changed=False, commands=None, failed=False, sort=False, **args):
        from ansible_collections.ale.aos8.tests.unit.modules.utils import set_module_args

        set_module_args(args)
        result = self.execute_module(changed=changed, commands=commands, failed=failed, sort=sort)
        if not failed and args.get("state", "merged") in ("merged", "replaced", "overridden", "deleted"):
            if changed:
                self.connection.edit_config.assert_called_once()
                sent = self.connection.edit_config.call_args[0][0]
                self.assertEqual(self.hide_secrets(sent), result["commands"])
            else:
                self.connection.edit_config.assert_not_called()
        return result

    def run_module_check(self, **args):
        from ansible_collections.ale.aos8.tests.unit.modules.utils import set_module_args

        args["_ansible_check_mode"] = True
        set_module_args(args)
        result = self.execute_module(changed=True)
        self.connection.edit_config.assert_not_called()
        self.assertNotIn("after", result)
        return result

#
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
#
from __future__ import absolute_import, division, print_function


__metaclass__ = type


from ansible.utils.display import Display
from ansible_collections.ansible.netcommon.plugins.action.network import (
    ActionModule as ActionNetworkModule,
)


display = Display()


class ActionModule(ActionNetworkModule):
    def run(self, tmp=None, task_vars=None):
        del tmp  # tmp no longer has any effect

        module_name = self._task.action.split(".")[-1]
        self._config_module = True if module_name in ["aos8_config", "config"] else False
        persistent_connection = self._play_context.connection.split(".")[-1]
        warnings = []

        if persistent_connection != "network_cli":
            return {
                "failed": True,
                "msg": "Connection type %s is not valid for this module"
                % self._play_context.connection,
            }

        result = super(ActionModule, self).run(task_vars=task_vars)
        if warnings:
            if "warnings" in result:
                result["warnings"].extend(warnings)
            else:
                result["warnings"] = warnings
        return result

    def _handle_backup_option(self, result, task_vars, backup_options):
        # ansible.netcommon replaces "changed" with whether the backup file was
        # written, so a configuration change was reported as not changed when the
        # backup file already held the same content. Keep the module result.
        module_changed = result.get("changed", False)
        super(ActionModule, self)._handle_backup_option(result, task_vars, backup_options)
        result["changed"] = bool(module_changed or result.get("changed"))

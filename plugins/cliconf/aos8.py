# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
author:
  - Samuel Yip Kah Yean (@samuelyip74)
  - Mathias Guillemot (@mathias-gt)
name: aos8
short_description: Use aos8 cliconf to run commands on Alcatel-Lucent Enterprise AOS 8 devices
description:
  - This aos8 plugin provides low level abstraction APIs for sending and receiving CLI
    commands from Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
  - The switch must run from the working directory. Configuration changes are refused when
    it runs from the certified directory.
version_added: 1.0.0
options:
  write_memory_flag:
    type: boolean
    default: true
    description:
      - Saves the configuration to flash with C(write memory flash-synchro) after each change
        made by a resource module or by M(ale.aos8.aos8_config).
      - The command can take a long time, so C(ansible_command_timeout) must be 60 seconds or more
        when this option is enabled.
    env:
      - name: ANSIBLE_AOS_WRITE_MEMORY_FLASH
    vars:
      - name: ansible_aos_write_memory_flash
  flash_synchro_flag:
    type: boolean
    default: false
    description:
      - Runs C(copy running certified flash-synchro) after each change, to copy the running
        directory to the certified directory and synchronize them.
      - C(ansible_command_timeout) must be 60 seconds or more when this option is enabled.
    env:
      - name: ANSIBLE_AOS_FLASH_SYNCHRO_FLAG
    vars:
      - name: ansible_aos_flash_synchro_flag
"""

EXAMPLES = """
# Inventory variables for a switch managed with this collection
#
# ansible_connection: ansible.netcommon.network_cli
# ansible_network_os: ale.aos8.aos8
# ansible_command_timeout: 90
# ansible_aos_write_memory_flash: true
# ansible_aos_flash_synchro_flag: false

- name: Change the system name and save the configuration to flash
  ale.aos8.aos8_hostname:
    config:
      hostname: val-os1-saved
    state: merged
  vars:
    ansible_aos_write_memory_flash: true
    ansible_command_timeout: 90

- name: Change the system name without saving it
  ale.aos8.aos8_hostname:
    config:
      hostname: val-os1
    state: merged
  vars:
    ansible_aos_write_memory_flash: false

- name: Change the system name, save it and synchronize the certified directory
  ale.aos8.aos8_hostname:
    config:
      hostname: val-os1-synchro
    state: merged
  vars:
    ansible_aos_write_memory_flash: true
    ansible_aos_flash_synchro_flag: true
    ansible_command_timeout: 90
"""

import json
import re

from collections.abc import Mapping

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.config import (
    NetworkConfig,
    dumps,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_list
from ansible_collections.ansible.netcommon.plugins.plugin_utils.cliconf_base import (
    CliconfBase,
)


class Cliconf(CliconfBase):
    def __init__(self, *args, **kwargs):
        self._device_info = {}
        super(Cliconf, self).__init__(*args, **kwargs)

    def get_config(self, source="running", flags=None, format=None):
        if source != "running":
            raise ValueError("fetching configuration from %s is not supported" % source)

        if format:
            raise ValueError("'format' value %s is not supported for get_config" % format)

        if not flags:
            flags = []
        cmd = "show configuration snapshot "

        cmd += " ".join(to_list(flags))
        cmd = cmd.strip()

        return self.send_command(cmd)

    def get_diff(
        self,
        candidate=None,
        running=None,
        diff_match="line",
        diff_ignore_lines=None,
        path=None,
        diff_replace="line",
    ):
        diff = {}
        device_operations = self.get_device_operations()
        option_values = self.get_option_values()

        if candidate is None and device_operations["supports_generate_diff"]:
            raise ValueError(
                "candidate configuration is required to generate diff",
            )

        if diff_match not in option_values["diff_match"]:
            raise ValueError(
                "'match' value %s in invalid, valid values are %s"
                % (diff_match, ", ".join(option_values["diff_match"])),
            )

        if diff_replace not in option_values["diff_replace"]:
            raise ValueError(
                "'replace' value %s in invalid, valid values are %s"
                % (diff_replace, ", ".join(option_values["diff_replace"])),
            )

        # prepare candidate configuration
        candidate_obj = NetworkConfig(indent=3)
        candidate_obj.load(candidate)

        if running and diff_match != "none" and diff_replace != "config":
            # running configuration
            running_obj = NetworkConfig(
                indent=3,
                contents=running,
                ignore_lines=diff_ignore_lines,
            )
            configdiffobjs = candidate_obj.difference(
                running_obj,
                path=path,
                match=diff_match,
                replace=diff_replace,
            )

        else:
            configdiffobjs = candidate_obj.items

        diff["config_diff"] = dumps(configdiffobjs, "commands") if configdiffobjs else ""
        return diff

    def edit_config(self, candidate=None, commit=True, replace=None, comment=None):
        resp = {}
        operations = self.get_device_operations()
        self.check_edit_config_capability(operations, candidate, commit, replace, comment)

        results = []
        requests = []

        running_directory = self.check_running_directory()
        if running_directory is None:
            raise ValueError("Unable to read the running directory of the switch")
        if running_directory == "CERTIFIED":
            raise ValueError(
                "The switch runs from the certified directory: configuration changes cannot be saved",
            )

        for line in to_list(candidate):
            if not isinstance(line, Mapping):
                line = {"command": line}
            cmd = line["command"]
            if cmd != "exit" and cmd[0] != "!":
                results.append(self.send_command(**line))
                requests.append(cmd)

        if commit:
            if self.get_option("write_memory_flag"):
                self.write_memory()
            if self.get_option("flash_synchro_flag"):
                self.flash_synchro()

        resp["request"] = requests
        resp["response"] = results
        return resp

    def get(
        self,
        command=None,
        prompt=None,
        answer=None,
        sendonly=False,
        newline=True,
        output=None,
        check_all=False,
    ):
        if not command:
            raise ValueError("must provide value of command to execute")
        if output:
            raise ValueError("'output' value %s is not supported for get" % output)

        return self.send_command(
            command=command,
            prompt=prompt,
            answer=answer,
            sendonly=sendonly,
            newline=newline,
            check_all=check_all,
        )

    def check_running_directory(self):
        """Returns the directory the switch runs from: WORKING, CERTIFIED or a user directory."""
        reply = self.get(command="show running-directory")
        data = to_text(reply, errors="surrogate_or_strict").strip()
        match = re.search(r"Running configuration\s*:\s(.*)\,", data)
        if match:
            return match.group(1)
        return None

    def _check_timeout(self, minimum):
        timeout = self._connection.get_option("persistent_command_timeout")
        if timeout < minimum:
            raise ValueError(
                "ansible_command_timeout must be %s seconds or more to save the configuration"
                % minimum,
            )

    def write_memory(self):
        """Saves the running configuration to the running directory."""
        self._check_timeout(60)
        self.get(command="write memory flash-synchro")
        data = to_text(self.get(command="show running-directory"), errors="surrogate_or_strict")
        if re.search(r"NOT SYNCHRONIZED", data):
            raise ValueError("The configuration was not saved to flash")
        return True

    def flash_synchro(self):
        """Copies the running directory to the certified directory and synchronizes them."""
        self._check_timeout(60)
        self.get(command="copy running certified flash-synchro")
        data = to_text(self.get(command="show running-directory"), errors="surrogate_or_strict")
        if re.search(r"CERTIFY NEEDED", data):
            raise ValueError("Certified directory not synchronized")
        return True

    # Return the basic information about the device.  Model / Version and Up time
    def get_device_info(self):
        if not self._device_info:
            device_info = {}
            device_info["network_os"] = "aos8"
            reply = self.get(command="show system")
            data = to_text(reply, errors="surrogate_or_strict").strip()
            match = re.search(r"Alcatel-Lucent Enterprise\s([\w\s]+\-[\w]+)\s([0-9.RAG\s]+)\,", data)
            if match:
                device_info["network_os_model"] = match.group(1)
                device_info["network_os_version"] = match.group(2)
            match = re.search(r"Up Time:\s+(.*)\,", data, re.M)
            if match:
                device_info["network_os_uptime"] = match.group(1)
            self._device_info = device_info
        return self._device_info

    def get_device_operations(self):
        return {
            "supports_diff_replace": True,
            "supports_commit": False,
            "supports_rollback": False,
            "supports_defaults": True,
            "supports_onbox_diff": False,
            "supports_commit_comment": False,
            "supports_multiline_delimiter": True,
            "supports_diff_match": True,
            "supports_diff_ignore_lines": True,
            "supports_generate_diff": True,
            "supports_replace": False,
        }

    def get_option_values(self):
        return {
            "format": ["text"],
            "diff_match": ["line", "strict", "exact", "none"],
            "diff_replace": ["line", "block"],
            "output": [],
        }

    def get_capabilities(self):
        result = super(Cliconf, self).get_capabilities()
        # result["rpc"] += ["edit_banner", "get_diff", "run_commands", "get_defaults_flag"]
        result["device_operations"] = self.get_device_operations()
        result.update(self.get_option_values())
        return json.dumps(result)

    def run_commands(self, commands=None, check_rc=True):
        if commands is None:
            raise ValueError("'commands' value is required")

        responses = list()
        for cmd in to_list(commands):
            if not isinstance(cmd, Mapping):
                cmd = {"command": cmd}

            output = cmd.pop("output", None)
            if output:
                raise ValueError("'output' value %s is not supported for run_commands" % output)

            try:
                out = self.send_command(**cmd)
            except AnsibleConnectionFailure as e:
                if check_rc:
                    raise
                out = getattr(e, "err", to_text(e))

            responses.append(out)

        return responses

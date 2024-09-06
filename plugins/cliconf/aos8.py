#
# (c) 2017 Red Hat Inc.
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

DOCUMENTATION = """
author:
- Samuel Yip (@samuelyip74)
name: AOS8
short_description: Use AOS8 cliconf to run command on Alcatel-Lucent Enterprise AOS 8 platform
description:
- This AOS8 plugin provides low level abstraction apis for sending and receiving CLI
  commands from Alcatel-Lucent Enterprise AOS 8 network devices.
version_added: 1.0.0
options:
  write_memory_flag:
    type: boolean
    default: true
    description:
    - True or false to save configuration into flash
    env:
    - name: ANSIBLE_AOS_WRITE_MEMORY_FLASH
    vars:
    - name: ansible_aos_write_memory_flash
  flash_synchro_flag:
    type: boolean
    default: false
    description:
    - True or false to copy sync working and certified directories.
    env:
    - name: ANSIBLE_AOS_FLASH_SYNCHRO_FLAG
    vars:
    - name: ansible_aos_flash_synchro_flag    

"""

EXAMPLES = """

- name: Example commit confirmed
  vars:
    ansible_aos_write_memory_flash: true
    ansible_aos_flash_synchro_flag: false
  tasks:
    - name: "Commit confirmed with timeout"
      ale.aos8.aos8_hostname:
        state: merged
        config:
          hostname: R1

"""

import json
import re
import time

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils._text import to_text
from ansible.module_utils.common._collections_compat import Mapping
from ansible.module_utils.six import iteritems
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
        if source not in ("running", "startup"):
            raise ValueError("fetching configuration from %s is not supported" % source)

        if format:
            raise ValueError("'format' value %s is not supported for get_config" % format)

        if not flags:
            flags = []
        if source == "running":
            cmd = "show configuration snapshot "
        else:
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
    # def get_diff(
    #     self,
    #     candidate=None,
    #     running=None,
    #     diff_match="line",
    #     diff_ignore_lines=None,
    #     path=None,
    #     diff_replace="line",
    # ):
    #     """
    #     Generate diff between candidate and running configuration. If the
    #     remote host supports onbox diff capabilities ie. supports_onbox_diff in that case
    #     candidate and running configurations are not required to be passed as argument.
    #     In case if onbox diff capability is not supported candidate argument is mandatory
    #     and running argument is optional.
    #     :param candidate: The configuration which is expected to be present on remote host.
    #     :param running: The base configuration which is used to generate diff.
    #     :param diff_match: Instructs how to match the candidate configuration with current device configuration
    #                   Valid values are 'line', 'strict', 'exact', 'none'.
    #                   'line' - commands are matched line by line
    #                   'strict' - command lines are matched with respect to position
    #                   'exact' - command lines must be an equal match
    #                   'none' - will not compare the candidate configuration with the running configuration
    #     :param diff_ignore_lines: Use this argument to specify one or more lines that should be
    #                               ignored during the diff.  This is used for lines in the configuration
    #                               that are automatically updated by the system.  This argument takes
    #                               a list of regular expressions or exact line matches.
    #     :param path: The ordered set of parents that uniquely identify the section or hierarchy
    #                  the commands should be checked against.  If the parents argument
    #                  is omitted, the commands are checked against the set of top
    #                 level or global commands.
    #     :param diff_replace: Instructs on the way to perform the configuration on the device.
    #                     If the replace argument is set to I(line) then the modified lines are
    #                     pushed to the device in configuration mode.  If the replace argument is
    #                     set to I(block) then the entire command block is pushed to the device in
    #                     configuration mode if any line is not correct.
    #     :return: Configuration diff in  json format.
    #            {
    #                'config_diff': '',
    #                'banner_diff': {}
    #            }
    #     """
    #     diff = {}
    #     device_operations = self.get_device_operations()
    #     option_values = self.get_option_values()

    #     if candidate is None and device_operations["supports_generate_diff"]:
    #         raise ValueError("candidate configuration is required to generate diff")

    #     if diff_match not in option_values["diff_match"]:
    #         raise ValueError(
    #             "'match' value %s in invalid, valid values are %s"
    #             % (diff_match, ", ".join(option_values["diff_match"])),
    #         )

    #     if diff_replace not in option_values["diff_replace"]:
    #         raise ValueError(
    #             "'replace' value %s in invalid, valid values are %s"
    #             % (diff_replace, ", ".join(option_values["diff_replace"])),
    #         )

    #     # prepare candidate configuration
    #     candidate_obj = NetworkConfig(indent=1)
    #     want_src, want_banners = self._extract_banners(candidate)
    #     candidate_obj.load(want_src)

    #     if running and diff_match != "none":
    #         # running configuration
    #         have_src, have_banners = self._extract_banners(running)
    #         running_obj = NetworkConfig(indent=1, contents=have_src, ignore_lines=diff_ignore_lines)
    #         configdiffobjs = candidate_obj.difference(
    #             running_obj,
    #             path=path,
    #             match=diff_match,
    #             replace=diff_replace,
    #         )

    #     else:
    #         configdiffobjs = candidate_obj.items
    #         have_banners = {}

    #     diff["config_diff"] = dumps(configdiffobjs, "commands") if configdiffobjs else ""
    #     banners = self._diff_banners(want_banners, have_banners)
    #     diff["banner_diff"] = banners if banners else {}
    #     return diff

    def edit_config(self, candidate=None, commit=True, replace=None, comment=None):
        resp = {}
        operations = self.get_device_operations()
        self.check_edit_config_capability(operations, candidate, commit, replace, comment)

        results = []
        requests = []

        device_running_directory_state = self.check_running_directory()
        # check if device is running configuration from working directory.
        if device_running_directory_state is None:
            raise ValueError("Device not ready!")
        elif device_running_directory_state == "WORKING":
            for line in to_list(candidate):
                if not isinstance(line, Mapping):
                    line = {"command": line}
                cmd = line["command"]
                if cmd != "exit" and cmd[0] != "!":
                    results.append(self.send_command(**line))
                    requests.append(cmd) 

            if commit:      
                # save configuration into flash (working directory) if write_memory_flag: true
                if self.get_option("write_memory_flag"):
                    self.write_memory()

                # copy working directory to certify directory if  flash_synchro_flag: true
                if self.get_option("flash_synchro_flag"):
                    self.flash_sychro()
             
  
        else:
            raise ValueError("Device in CERTIFIED mode")

        resp["request"] = requests
        resp["response"] = results
        return resp

    # def edit_macro(self, candidate=None, commit=True, replace=None, comment=None):
    #     """
    #     ios_config:
    #       lines: "{{ macro_lines }}"
    #       parents: "macro name {{ macro_name }}"
    #       after: '@'
    #       match: line
    #       replace: block
    #     """
    #     resp = {}
    #     operations = self.get_device_operations()
    #     self.check_edit_config_capability(operations, candidate, commit, replace, comment)

    #     results = []
    #     requests = []
    #     if commit:
    #         commands = ""
    #         self.send_command("config terminal")
    #         time.sleep(0.1)
    #         # first item: macro command
    #         commands += candidate.pop(0) + "\n"
    #         multiline_delimiter = candidate.pop(-1)
    #         for line in candidate:
    #             commands += " " + line + "\n"
    #         commands += multiline_delimiter + "\n"
    #         obj = {"command": commands, "sendonly": True}
    #         results.append(self.send_command(**obj))
    #         requests.append(commands)

    #         time.sleep(0.1)
    #         self.send_command("end", sendonly=True)
    #         time.sleep(0.1)
    #         results.append(self.send_command("\n"))
    #         requests.append("\n")

    #     resp["request"] = requests
    #     resp["response"] = results
    #     return resp

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

    # Return the running mode: WORKING OR CERTIFIED
    def check_running_directory(self):
        reply = self.get(command="show running-directory")
        data = to_text(reply, errors="surrogate_or_strict").strip()
        match = re.search(r"Running configuration\s*:\s(.*)\,", data)
        if match:
            return match.group(1)
        else:
            return None

    # Save configuration and raise error if configuration not synchronize.
    def write_memory(self):
        persistent_command_timeout = self._connection.get_option("persistent_command_timeout")
        if persistent_command_timeout < 60:
            raise ValueError(
                "ansible_command_timeout can't be less than 60 seconds."
                "Please adjust and try again",
            )

        reply = self.get(command="write memory flash-synchro")
        reply = self.get(command="show running-directory")
        data = to_text(reply, errors="surrogate_or_strict").strip()
        match = re.search(r"NOT SYNCHRONIZED", data)
        if match:
            raise ValueError("Configuration not synchronized.")
        else:
            return True

    def flash_sychro(self):
        persistent_command_timeout = self._connection.get_option("persistent_command_timeout")        
        if persistent_command_timeout < 60:
            raise ValueError(
                "ansible_command_timeout can't be less than 60 seconds."
                "Please adjust and try again",
            )

        reply = self.get(command="copy flash-synchro")
        reply = self.get(command="show running-directory")
        data = to_text(reply, errors="surrogate_or_strict").strip()
        match = re.search(r"CERTIFY NEEDED", data)
        if match:
            raise ValueError("Certified directory not synchronized.")
        else:
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

    def get_defaults_flag(self):
        """
        The method identifies the filter that should be used to fetch running-configuration
        with defaults.
        :return: valid default filter
        """
        out = self.get("show configuration snapshot")
        out = to_text(out, errors="surrogate_then_replace")

        commands = set()
        for line in out.splitlines():
            if line.strip():
                commands.add(line.strip().split()[0])

        if "all" in commands:
            return "all"
        else:
            return "full"

    def _diff_banners(self, want, have):
        candidate = {}
        for key, value in iteritems(want):
            if value != have.get(key):
                candidate[key] = value
        return candidate

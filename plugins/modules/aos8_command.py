#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_command
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_command
short_description: Run commands on AOS 8 devices
description:
  - Sends commands to an Alcatel-Lucent Enterprise OmniSwitch running AOS 8 and returns the output.
  - The module always reports C(changed=false), also when a command changes the configuration. Use M(ale.aos8.aos8_config)
    or the resource modules to configure the switch.
  - In check mode, only commands that start with C(show) are sent.
version_added: 1.0.0
author:
  - Samuel Yip Kah Yean (@samuelyip74)
  - Mathias Guillemot (@mathias-gt)
notes:
  - Tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.
  - This module works with connection C(ansible.netcommon.network_cli).
  - The task fails when the switch answers a command with an error.
options:
  commands:
    description:
      - List of commands to send to the switch. The output of each command is returned.
      - A command that asks for a confirmation is given as a dictionary with the keys C(command), C(prompt)
        (a regular expression that matches the question) and C(answer).
    type: list
    elements: raw
    required: true
"""

EXAMPLES = r"""
- name: Run a show command
  ale.aos8.aos8_command:
    commands: show system

- name: Run several commands
  ale.aos8.aos8_command:
    commands:
      - show vlan
      - show ip interface

- name: Run a command that changes the switch
  ale.aos8.aos8_command:
    commands:
      - interfaces port 1/1/20 admin-state disable

- name: Answer a confirmation question
  ale.aos8.aos8_command:
    commands:
      - command: no vlan 40
        prompt: '[Yy]/[Nn]'
        answer: y

- name: In check mode only show commands are sent
  ale.aos8.aos8_command:
    commands:
      - show vlan
      - vlan 41 admin-state enable
  check_mode: true
"""

RETURN = r"""
---
stdout:
  description: The output of each command.
  returned: always
  type: list
  elements: str
  sample:
    - |-
      System:
        Description:  Alcatel-Lucent Enterprise OS687024-SIM 8.11.162.R01 GA
stdout_lines:
  description: The output of each command, split into lines.
  returned: always
  type: list
  elements: list
  sample:
    - - 'System:'
      - '  Description:  Alcatel-Lucent Enterprise OS687024-SIM 8.11.162.R01 GA'
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    to_lines,
    transform_commands,
)

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.aos8 import run_commands
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.command.command import (
    CommandArgs,
)


def parse_commands(module):
    commands = transform_commands(module)
    if module.check_mode:
        for item in list(commands):
            if not item["command"].startswith("show"):
                module.warn(
                    "Only show commands are supported when using check mode, not executing %s"
                    % item["command"],
                )
                commands.remove(item)
    return commands


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=CommandArgs.argument_spec,
        supports_check_mode=True,
    )
    commands = parse_commands(module)
    responses = run_commands(module, commands)
    module.exit_json(changed=False, stdout=responses, stdout_lines=list(to_lines(responses)))


if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_command
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
GENERATOR_VERSION: '1.0'

NETWORK_OS: aos8
RESOURCE: command
COPYRIGHT: Copyright 2019 Red Hat
LICENSE: gpl-3.0.txt

DOCUMENTATION: |
module: aos8_command
author: Samuel Yip Kah Yean (@samuelyip74)
short_description: Module to run commands on remote devices.
description:
  - Sends arbitrary commands to an aos8 node and returns the results read from the device.
    This module includes an argument that will cause the module to wait for a specific
    condition before returning or timing out if the condition is not met.
  - This module does not automatically save the configuration into memory and flash. 
version_added: 1.0.0
notes:
  - Tested against Alcatel AOS8 8.9.221.R03 GA.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_aos8.html)
options:
  commands:
    description:
      - List of commands to send to the remote aos8 device over the configured provider.
        The resulting output from the command is returned. If the I(wait_for) argument
        is provided, the module is not returned until the condition is satisfied or
        the number of retries has expired. If a command sent to the device requires
        answering a prompt, it is possible to pass a dict containing I(command), I(answer)
        and I(prompt). Common answers are 'y' or "\\r" (carriage return, must be double
        quotes). See examples.
    required: true
    type: list
    elements: raw
  output:
    description:
      - Print the output of the command(s), if any.
    aliases:
      - output
    type: list
    elements: str

EXAMPLES:
- name: Run show system on remote devices
  alcatel.aos8.aos8_command:
    commands: show system

- name: Run multiple commands on remote nodes
  alcatel.aos8.aos8_command:
    commands:
      - show system
      - show interfaces

"""

EXAMPLES = r"""

- name: Run show system command on remote nodes
  alcatel.aos8.aos8_command:
    commands:
      - show system 

# output-
#ok: [aos8appliance] => {
#    "changed": false,
#    "invocation": {
#        "module_args": {
#            "commands": [
#                "show system"
#            ],
#            "output": [
#                [
#                    "System:",
#                    "  Description:  Alcatel-Lucent Enterprise OS6860E-P24 8.9.221.R03 GA, October 12, 2023.,",
#                    "  Object ID:    1.3.6.1.4.1.6486.801.1.1.2.1.11.1.6,",
#                    "  Up Time:      22 days 22 hours 8 minutes and 21 seconds,",
#                    "  Contact:      ,",
#                    "  Name:         
#                    "  Location:     ,",
#                    "  Services:     78,",
#                    "  Date & Time:  WED DEC 13 2023 23:11:06 (ZP8)",
#                    "Flash Space:",
#                    "    Primary CMM:",
#                    "      Available (bytes):  803958784,",
#                    "      Comments         :  None"
#                ]
#            ]
#        }
#    },
#    "stdout": [
#        "System:\n  Description:  Alcatel-Lucent Enterprise OS6860E-P24 8.9.221.R03 GA, October 12, 2023.,\n  Object ID:    1.3.6.1.4.1.6486.801.1.1.2.1.11.1.6,\n  Up Time:      22 days 22 hours 8 minutes and 21 seconds,\n  Contact:      ,\n  Name:         \n  Location:     ,\n  Services:     78,\n  Date & Time:  WED DEC 13 2023 23:11:06 (ZP8)\nFlash Space:\n    Primary CMM:\n      Available (bytes):  803958784,\n      Comments         :  None"
#    ],
#    "stdout_lines": [
#        [
#            "System:",
#            "  Description:  Alcatel-Lucent Enterprise OS6860E-P24 8.9.221.R03 GA, October 12, 2023.,",
#            "  Object ID:    1.3.6.1.4.1.6486.801.1.1.2.1.11.1.6,",
#            "  Up Time:      22 days 22 hours 8 minutes and 21 seconds,",
#            "  Contact:      ,",
#            "  Name:         
#            "  Location:     b,",
#            "  Services:     78,",
#            "  Date & Time:  WED DEC 13 2023 23:11:06 (ZP8)",
#            "Flash Space:",
#            "    Primary CMM:",
#            "      Available (bytes):  803958784,",
#            "      Comments         :  None"
#        ]
#    ]


- name: Run multiple commands on remote nodes
  alcatel.aos8.aos8_command:
    commands:
      - show system 
      - show ip interface
      
# output-
#ok: [aos8appliance] => {
#    "changed": false,
#    "invocation": {
#        "module_args": {
#            "commands": [
#                "show system",
#                "show ip interface"
#            ],
#            "output": [
#                [
#                    "System:",
#                    "  Description:  Alcatel-Lucent Enterprise OS6860E-P24 8.9.221.R03 GA, October 12, 2023.,",
#                    "  Object ID:    1.3.6.1.4.1.6486.801.1.1.2.1.11.1.6,",
#                    "  Up Time:      22 days 22 hours 13 minutes and 13 seconds,",
#                    "  Contact:      ,",
#                    "  Name:         
#                    "  Location:     
#                    "  Services:     78,",
#                    "  Date & Time:  WED DEC 13 2023 23:15:58 (ZP8)",
#                    "Flash Space:",
#                    "    Primary CMM:",
#                    "      Available (bytes):  803958784,",
#                    "      Comments         :  None"
#                ],
#                [
#                    "Total 6 interfaces",
#                    " Flags (D=Directly-bound)",
#                    "",
#                    "            Name                 IP Address      Subnet Mask     Status Forward  Device   Flags",
#                    "--------------------------------+---------------+---------------+------+-------+---------+------",
#                    "EMP-CHAS1                        11.1.1.1        255.255.255.0   DOWN   NO      EMP         ",
#                    "EMP-CMMA-CHAS1                   0.0.0.0         0.0.0.0         DOWN   NO      EMP         ",
#                    "Loopback                         127.0.0.1       255.255.255.255 UP     NO      Loopback    ",
#                    "Loopback0                        10.0.0.4        255.255.255.255 UP     YES     Loopback0    ",
#                    "int-33                           192.168.33.1    255.255.255.0   DOWN   NO      vlan 33     ",
#                    "int-vl1                          192.168.70.1    255.255.255.0   UP     NO      vlan 1"
#                ]
#            ]
#        }
#    },
#    "stdout": [
#        "System:\n  Description:  Alcatel-Lucent Enterprise OS6860E-P24 8.9.221.R03 GA, October 12, 2023.,\n  Object ID:    1.3.6.1.4.1.6486.801.1.1.2.1.11.1.6,\n  Up Time:      22 days 22 hours 13 minutes and 13 seconds,\n  Contact:      ,\n  Name:         ACSW01,\n  Location:     ALE Demo Lab,\n  Services:     78,\n  Date & Time:  WED DEC 13 2023 23:15:58 (ZP8)\nFlash Space:\n    Primary CMM:\n      Available (bytes):  803958784,\n      Comments         :  None",
#        "Total 6 interfaces\n Flags (D=Directly-bound)\n\n            Name                 IP Address      Subnet Mask     Status Forward  Device   Flags\n--------------------------------+---------------+---------------+------+-------+---------+------\nEMP-CHAS1                        11.1.1.1        255.255.255.0   DOWN   NO      EMP         \nEMP-CMMA-CHAS1                   0.0.0.0         0.0.0.0         DOWN   NO      EMP         \nLoopback                         127.0.0.1       255.255.255.255 UP     NO      Loopback    \nLoopback0                        10.0.0.4        255.255.255.255 UP     YES     Loopback0    \nint-33                           192.168.33.1    255.255.255.0   DOWN   NO      vlan 33     \nint-vl1                          192.168.70.1    255.255.255.0   UP     NO      vlan 1"
#    ],
#    "stdout_lines": [
#        [
#            "System:",
#            "  Description:  Alcatel-Lucent Enterprise OS6860E-P24 8.9.221.R03 GA, October 12, 2023.,",
#            "  Object ID:    1.3.6.1.4.1.6486.801.1.1.2.1.11.1.6,",
#            "  Up Time:      22 days 22 hours 13 minutes and 13 seconds,",
#            "  Contact:      ,",
#            "  Name:         
#            "  Location:     
#            "  Services:     78,",
#            "  Date & Time:  WED DEC 13 2023 23:15:58 (ZP8)",
#            "Flash Space:",
#            "    Primary CMM:",
#            "      Available (bytes):  803958784,",
#            "      Comments         :  None"
#        ],
#        [
#            "Total 6 interfaces",
#            " Flags (D=Directly-bound)",
#            "",
#            "            Name                 IP Address      Subnet Mask     Status Forward  Device   Flags",
#            "--------------------------------+---------------+---------------+------+-------+---------+------",
#            "EMP-CHAS1                        11.1.1.1        255.255.255.0   DOWN   NO      EMP         ",
#            "EMP-CMMA-CHAS1                   0.0.0.0         0.0.0.0         DOWN   NO      EMP         ",
#            "Loopback                         127.0.0.1       255.255.255.255 UP     NO      Loopback    ",
#            "Loopback0                        10.0.0.4        255.255.255.255 UP     YES     Loopback0    ",
#            "int-33                           192.168.33.1    255.255.255.0   DOWN   NO      vlan 33     ",
#            "int-vl1                          192.168.70.1    255.255.255.0   UP     NO      vlan 1"
#        ]
#    ]
#}


"""

import time
from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.parsing import (
    Conditional,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    to_lines,
    transform_commands,
)
from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.argspec.command.command import (
    CommandArgs,
)

from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.aos8 import run_commands

def parse_commands(module, warnings):
    commands = transform_commands(module)
    if module.check_mode:
        for item in list(commands):
            if not item["command"].startswith("show"):
                warnings.append(
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
    warnings = list()
    result = {"changed": False, "warnings": warnings}
    commands = parse_commands(module, warnings)
    responses = run_commands(module, commands)

    module.params["output"] = list(to_lines(responses))

    result.update({"stdout": responses, "stdout_lines": list(to_lines(responses))})
    module.exit_json(**result)

if __name__ == "__main__":
    main()

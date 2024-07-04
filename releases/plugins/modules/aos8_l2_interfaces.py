#!/usr/bin/python
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
"""
The module file for aos8_l2_interfaces
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: aos8_l2_interfaces
short_description: Resource module to configure VLAN membership on AOS8 devices
description:
  This module provides declarative management of l2 interfaces on Alcatel AOS8 network
  devices.
version_added: 1.0.0
author: Samuel Yip Kah Yean (@samuelyip74)
notes:
  - Tested against Alcatel-Lucent AOS8 OmniSwitch with Version 8.9.221.R03 GA.
  - This module works with connection C(network_cli).
options:
  config:
    description: A dictionary of VLANs options
    type: list
    elements: dict
    suboptions:
      vlan_id:
        description:
          - ID of the VLAN. Range 1-4094
        type: int
        required: true
      port_type:
        description:
          - The type of L2 interface
          - Refer to vendor documentation for valid values.
        type: str
        required: true
        choices:
          - port
          - linkagg        
      port_number:
        description:
          - The physical port number of logical linkagg number
        type: str
        required: true
      mode:
        description:
          - The type of encapsulation (802.1q or clear)
        type: str
        required: true
        choices:
          - untagged
          - tagged          
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the aos8 device
        by executing the command B(show vlan).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in
      - The states I(rendered), I(gathered) and I(parsed) does not perform any change
        on the device.
      - The state I(rendered) will transform the configuration in C(config) option to
        platform specific CLI commands which will be returned in the I(rendered) key
        within the result. For state I(rendered) active connection to remote host is
        not required.
      - The state I(gathered) will fetch the running configuration from device and transform
        it into structured data in the format as per the resource module argspec and
        the value is returned in the I(gathered) key within the result.
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into JSON format as per the resource module parameters and the
        value is returned in the I(parsed) key within the result. The value of C(running_config)
        option should be the same format as the output of command I(show running-config
        | include ip route|ipv6 route) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - rendered  
      - gathered
      - parsed
    default: merged
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# ACSW01-> show vlan 1 members
#    port      type        status
# ----------+-----------+---------------
#   1/1/26     untagged     forwarding
#   1/1/27     untagged     forwarding
#   1/1/28     untagged     forwarding


---
- hosts: all
  gather_facts: true
  ignore_errors: true
  name: L2 Interface merged with flash_synchro (true)
  vars:
    ansible_aos_flash_synchro_flag : true
  tasks:
    - name: Run L2 interfaces resource module with state merged
      alcatel.aos8.aos8_l2_interfaces:
        config:
          - vlan_id: 10
            port_type: port
            port_number: 1/1/27
            mode: untagged
        state: merged


# After state:
# ------------
# 
# ACSW01-> show vlan 10 members
#    port      type        status
# ----------+-----------+---------------
#   1/1/27     untagged      forwarding


# results : {
#     "after": [
#         {
#             "mode": "untagged",
#             "port_number": "1/1/28",
#             "port_type": "port",
#             "vlan_id": 1
#         },
#         {
#             "mode": "untagged",
#             "port_number": "1/1/27,
#             "port_type": "port",
#             "vlan_id": 10
#         },
#         {
#             "mode": "untagged",
#             "port_number": "1/1/26",
#             "port_type": "port",
#             "vlan_id": 1
#         },
#     ],
#     "changed": true,
#     "commands": [
#         "vlan 10 members port 1/1/27 untagged"
#     ],
#     "invocation": {
#         "module_args": {
#             "config": [
#                 {
#                     "mode": "untagged",
#                     "port_number": "1/1/27",
#                     "port_type": "port",
#                     "vlan_id": 10
#                 }
#             ],
#             "running_config": null,
#             "state": "merged"
#         }
#     }
# }

# Using overridden
#
# Before state:
# -------------
#
# ACSW01-> show vlan 1 members
#    port      type        status
# ----------+-----------+---------------
#   1/1/26     untagged     forwarding
#   1/1/27     untagged     forwarding
#   1/1/28     untagged     forwarding

---
- hosts: all
  gather_facts: true
  ignore_errors: true
  name: L2 Interface overridden with flash_synchro (true)
  vars:
    ansible_aos_flash_synchro_flag : true
  tasks:
    - name: Run L2 interfaces resource module with state overridden
      alcatel.aos8.aos8_l2_interfaces:
        config:
          - vlan_id: 1
            port_type: port
            port_number: 1/1/26
            mode: untagged
          - vlan_id: 10
            port_type: port
            port_number: 1/1/27
            mode: untagged
          - vlan_id: 1
            port_type: port
            port_number: 1/1/28
            mode: untagged                        
        state: overridden

# After state:
# ------------
# 
# ACSW01-> show vlan 10 members
#    port      type        status
# ----------+-----------+---------------
#   1/1/27     untagged      forwarding  

# results : {
#     "after": [
#         {
#             "mode": "untagged",
#             "port_number": "1/1/28",
#             "port_type": "port",
#             "vlan_id": 1
#         },
#         {
#             "mode": "untagged",
#             "port_number": "1/1/27,
#             "port_type": "port",
#             "vlan_id": 10
#         },
#         {
#             "mode": "untagged",
#             "port_number": "1/1/26",
#             "port_type": "port",
#             "vlan_id": 1
#         },
#     ],
#     "changed": true,
#     "commands": [
#         "vlan 10 members port 1/1/27 untagged"
#     ],
#     "invocation": {
#         "module_args": {
#             "config": [
#                 {
#                     "mode": "untagged",
#                     "port_number": "1/1/27",
#                     "port_type": "port",
#                     "vlan_id": 10
#                 }
#             ],
#             "running_config": null,
#             "state": "overridden"
#         }
#     }
# }
 
# Using deleted
#
# Before state:
# -------------
#
# ACSW01-> show vlan 10 members
#    port      type        status
# ----------+-----------+---------------
#   1/1/27     untagged     forwarding

---
- hosts: all
  gather_facts: true
  ignore_errors: true
  name: L2 Interface deleted with flash_synchro (true)
  vars:
    ansible_aos_flash_synchro_flag : false
  tasks:
    - name: Run L2 interfaces resource module with state deleted
      alcatel.aos8.aos8_l2_interfaces:
        config:
          - vlan_id: 10
            mode: tagged
            port_number: 1/1/27
            port_type: port
        state: deleted

# After state:
# -------------
# ACSW01-> show vlan 1 members
#    port      type        status
# ----------+-----------+---------------
#   1/1/26     untagged     forwarding
#   1/1/27     untagged     forwarding
#   1/1/28     untagged     forwarding   

# results: {
#     "after": [
#         {
#             "mode": "untagged",
#             "port_number": "1/1/28",
#             "port_type": "port",
#             "vlan_id": 1
#         },
#         {
#             "mode": "untagged",
#             "port_number": "1/1/27,
#             "port_type": "port",
#             "vlan_id": 1
#         },
#         {
#             "mode": "untagged",
#             "port_number": "1/1/26",
#             "port_type": "port",
#             "vlan_id": 1
#         },
#     ],
#     "changed": true,
#     "commands": [
#         "no vlan 10 members port 1/1/27"
#     ],
#     "invocation": {
#         "module_args": {
#             "config": [
#                 {
#                     "mode": "untagged",
#                     "port_number": "1/1/27",
#                     "port_type": "port",
#                     "vlan_id": 10
#                 }
#             ],
#             "running_config": null,
#             "state": "deleted"
#         }
#     }
# }

# Using Rendered
#
# Before state:
# -------------
#
# ACSW01-> show vlan 1 members
#    port      type        status
# ----------+-----------+---------------
#   1/1/26     untagged     forwarding
#   1/1/27     untagged     forwarding
#   1/1/28     untagged     forwarding
#
---
- hosts: all
  gather_facts: true
  ignore_errors: true
  name: L2 Interface rendered 
  vars:
    ansible_aos_flash_synchro_flag : true
  tasks:
    - name: Run L2 interfaces resource module with state rendered
      alcatel.aos8.aos8_l2_interfaces:
        config:
          - vlan_id: 10
            port_type: port
            port_number: 1/1/27
            mode: untagged  
        state: rendered

# results: {
#     "after": [
#     ],
#     "changed": false,
#     "commands": [
#         "vlan 10 members port 1/1/27 untagged"
#     ],
#     "invocation": {
#         "module_args": {
#             "config": [
#                 {
#                     "mode": "untagged",
#                     "port_number": "1/1/27",
#                     "port_type": "port",
#                     "vlan_id": 10
#                 }
#             ],
#             "running_config": null,
#             "state": "deleted"
#         }
#     }
# }

"""

RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['vlan 10 member 1/1/1 untagged', 'vlan 10 member 1/1/1 tagged']
"""
from ansible.module_utils.basic import AnsibleModule

from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.argspec.l2_interfaces.l2_interfaces import (
    L2_interfacesArgs,
)
from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.config.l2_interfaces.l2_interfaces import L2_interfaces


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "overridden", ("config",)),
        ("state", "rendered", ("config",)),           
        ("state", "parsed", ("running_config",)),     ### TODO: yet to be implemented
    ]
    mutually_exclusive = [("config", "running_config")]

    module = AnsibleModule(
        argument_spec=L2_interfacesArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )

    result = L2_interfaces(module).execute_module()
    module.exit_json(**result)

if __name__ == "__main__":
    main()
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
The module file for aos8_l3_interfaces
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: aos8_l3_interfaces
short_description: Resource module to configure Layer 3 interface on AOS8 devices
description:
  This module provides declarative management of l3 interfaces on Alcatel AOS8 network
  devices.
version_added: 1.0.0
author: Samuel Yip Kah Yean (@samuelyip74)
notes:
  - Tested against Alcatel-Lucent AOS8 OmniSwitch with Version 8.9.221.R03 GA.
  - This module works with connection C(network_cli).
options:
  config:
    description: A list of dictionary for L3 interface options
    type: list
    elements: dict
    suboptions:
      vrf:
        description:
          - The unique name of the VRF instance
        type: string
        required: false
      name:
        description:
          - The unique name of the IP interface
        type: str
        required: true
        choices:
          - port
          - linkagg        
      address:
        description:
          - The IP address of the interface
        type: str
        required: true
      mask:
        description:
          - The subnet mask of the interface
        type: str
        required: false
        choices:
          - untagged
          - tagged  
      type:
        description:
          - The type of layer 3 interface
        type: str
        required: false
        choices:
          - vlan
          - rtr-port
          - tunnel     
      port_id:
        description:
          - The vlan id, port number of the interface
        type: str
        required: false                       
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the aos8 device
        by executing the command B(show configuration | grep "ip interface").
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
# ip interface "Loopback0" address 10.1.1.1
# ip interface "intvlan1" address 192.168.1.1 mask 255.255.255.0 vlan 1 
# vrf MGNT ip interface "L3VPN" address 192.168.1.1 mask 255.255.255.0 vlan 51


---
- hosts: all
  gather_facts: true
  ignore_errors: true
  name: L3 Interface merged with flash_synchro (true)
  vars:
    ansible_aos_write_memory_flash  : false
    ansible_aos_flash_synchro_flag : false
  tasks:
    - name: Run L3 interfaces resource module with state merged
      alcatel.aos8.aos8_l3_interfaces:
        config:
          - name: intvlan33
            address: 192.168.33.1
            mask: 255.255.255.0
            type: vlan
            port_id: 33
        state: merged


# After state:
# ------------
# 
# ip interface "Loopback0" address 10.1.1.1
# ip interface "intvlan1" address 192.168.1.1 mask 255.255.255.0 vlan 1 
# ip interface "intvlan33" address 192.168.33.1 mask 255.255.255.0 vlan 33 
# vrf MGNT ip interface "L3VPN" address 192.168.1.1 mask 255.255.255.0 vlan 51


# results : {
#     "after": [
#         {
#             "name": "Loopback0",
#             "address": "10.1.1.1",
#         },
#         {
#             "name": "intvlan1",
#             "address": "192.168.1.1",
#             "mask": "255.255.255.0",
#             "type": "vlan",
#             "port_id": "1",
#         },
#         {
#             "name": "intvlan33",
#             "address": "192.168.33.1",
#             "mask": "255.255.255.0",
#             "type": "vlan",
#             "port_id": "33",
#         },
#         {
#             "vrf": "MGNT",
#             "name": "L3VPN",
#             "address": "192.168.1.1",
#             "mask": "255.255.255.0",
#             "type": "vlan",
#             "port_id": "51",
#         },
#     ],
#     "changed": true,
#     "commands": [
#         "ip interface intvlan33 address 192.168.33.1 mask 255.255.255.0 vlan 33"
#     ],
#     "invocation": {
#         "module_args": {
#             "config": [
#                 {
#                   "name": "intvlan33",
#                   "address": "192.168.33.1",
#                   "mask": "255.255.255.0",
#                   "type": "vlan",
#                   "port_id": "33",
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
# ip interface "Loopback0" address 10.1.1.1
# ip interface "intvlan1" address 192.168.1.1 mask 255.255.255.0 vlan 1 
# vrf MGNT ip interface "L3VPN" address 192.168.1.1 mask 255.255.255.0 vlan 51

---
- hosts: all
  gather_facts: true
  ignore_errors: true
  name: L3 Interface overridden with flash_synchro (true)
  vars:
    ansible_aos_flash_synchro_flag : true
  tasks:
    - name: Run L3 interfaces resource module with state overridden
      alcatel.aos8.aos8_l3_interfaces:
        config:
          - name: intvlan1
            address: 192.168.1.1
            mask: 255.255.255.0
            type: vlan
            port_id: 1
          - name: Loopback0
            address: 10.2.1.1
          - name: L3VPN
            address: 192.168.1.1
            mask: 255.255.255.0
            type: vlan
            port_id: 51
            vrf: MGNT                                             
        state: overridden

# After state:
# ------------
# 
# ip interface "Loopback0" address 10.2.1.1
# ip interface "intvlan1" address 192.168.1.1 mask 255.255.255.0 vlan 1 
# vrf MGNT ip interface "L3VPN" address 192.168.1.1 mask 255.255.255.0 vlan 51

# results : {
#     "after": [
#         {
#             "name": "Loopback0",
#             "address": "10.2.1.1",
#         },
#         {
#             "name": "intvlan1",
#             "address": "192.168.1.1",
#             "mask": "255.255.255.0",
#             "type": "vlan",
#             "port_id": "1",
#         },
#         {
#             "vrf": "MGNT",
#             "name": "L3VPN",
#             "address": "192.168.1.1",
#             "mask": "255.255.255.0",
#             "type": "vlan",
#             "port_id": "51",
#         },
#     ],
#     "changed": true,
#     "commands": [
#         "ip interface Loopback0 10.2.1.1"
#     ],
#     "invocation": {
#         "module_args": {
#             "config": [
#                 {
#                   "name": "Loopback0",
#                   "address": "10.2.1.1",
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
# ip interface "Loopback0" address 10.1.1.1
# ip interface "intvlan1" address 192.168.1.1 mask 255.255.255.0 vlan 1 
# ip interface "intvlan33" address 192.168.33.1 mask 255.255.255.0 vlan 33 
# vrf MGNT ip interface "L3VPN" address 192.168.1.1 mask 255.255.255.0 vlan 51

---
- hosts: all
  gather_facts: true
  ignore_errors: true
  name: L3 Interface deleted with flash_synchro (true)
  vars:
    ansible_aos_write_memory_flash  : false
    ansible_aos_flash_synchro_flag : false
  tasks:
    - name: Run L3 interfaces resource module with state deleted
      alcatel.aos8.aos8_l3_interfaces:
        config:
          - name: intvlan33
            address: 192.168.33.1
            mask: 255.255.255.0
            type: vlan
            port_id: 33
        state: deleted

# After state:
# -------------
# ip interface "Loopback0" address 10.1.1.1
# ip interface "intvlan1" address 192.168.1.1 mask 255.255.255.0 vlan 1 
# vrf MGNT ip interface "L3VPN" address 192.168.1.1 mask 255.255.255.0 vlan 51

# results: {
#     "after": [
#         {
#             "name": "Loopback0",
#             "address": "10.1.1.1",
#         },
#         {
#             "name": "intvlan1",
#             "address": "192.168.1.1",
#             "mask": "255.255.255.0",
#             "type": "vlan",
#             "port_id": "1",
#         },
#         {
#             "vrf": "MGNT",
#             "name": "L3VPN",
#             "address": "192.168.1.1",
#             "mask": "255.255.255.0",
#             "type": "vlan",
#             "port_id": "51",
#         },
#     ],
#     "changed": true,
#     "commands": [
#         "no ip interface intvlan33"
#     ],
#     "invocation": {
#         "module_args": {
#             "config": [
#                 {
#                   "name": "intvlan33",
#                   "address": "192.168.33.1",
#                   "mask": "255.255.255.0",
#                   "type": "vlan",
#                   "port_id": "33",
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
# ip interface "Loopback0" address 10.1.1.1
# ip interface "intvlan1" address 192.168.1.1 mask 255.255.255.0 vlan 1 
# vrf MGNT ip interface "L3VPN" address 192.168.1.1 mask 255.255.255.0 vlan 51
#
---
- hosts: all
  gather_facts: true
  ignore_errors: true
  name: L3 Interface rendered 
  vars:
    ansible_aos_write_memory_flash  : false
    ansible_aos_flash_synchro_flag : false
  tasks:
    - name: Run L3 interfaces resource module with state rendered
      alcatel.aos8.aos8_l3_interfaces:
        config:
          - name: intvlan33
            address: 192.168.33.1
            mask: 255.255.255.0
            type: vlan
            port_id: 33
        state: rendered

# results: {
#     "after": [
#     ],
#     "changed": false,
#     "commands": [
#         "ip interface intvlan33 address 192.168.33.1 mask 255.255.255.0 vlan 33"
#     ],
#     "invocation": {
#         "module_args": {
#             "config": [
#                 {
#                   "name": "intvlan33",
#                   "address": "192.168.33.1",
#                   "mask": "255.255.255.0",
#                   "type": "vlan",
#                   "port_id": "33",
#                 }
#             ],
#             "running_config": null,
#             "state": "rendered"
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
  sample: ['ip interface intvlan33 address 192.168.33.1 mask 255.255.255.0 vlan 33']
"""
from ansible.module_utils.basic import AnsibleModule

from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.argspec.l3_interfaces.l3_interfaces import (
    L3_interfacesArgs,
)
from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.config.l3_interfaces.l3_interfaces import L3_interfaces


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
        argument_spec=L3_interfacesArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )

    result = L3_interfaces(module).execute_module()
    module.exit_json(**result)

if __name__ == "__main__":
    main()


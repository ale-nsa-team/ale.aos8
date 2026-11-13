#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_l3_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_l3_interfaces
short_description: Resource module to configure IP interfaces
description:
  - This module manages IPv4 interfaces bound to a VLAN, and Loopback0, on Alcatel-Lucent Enterprise OmniSwitch
    devices running AOS 8.
  - Interfaces of other kinds (EMP, router ports, tunnels) are not read or changed by this module.
version_added: 1.0.0
author:
  - Samuel Yip Kah Yean (@samuelyip74)
  - Mathias Guillemot (@mathias-gt)
notes:
  - Tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.
  - This module works with connection C(ansible.netcommon.network_cli).
  - After a change, the configuration is saved to flash with C(write memory flash-synchro), unless C(ansible_aos_write_memory_flash)
    is set to C(false). Saving needs C(ansible_command_timeout) to be 60 seconds or more.
options:
  config:
    description:
      - A list of IP interfaces.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Name of the IP interface. An interface whose name starts with C(Loopback) only takes an address.
        type: str
        required: true
      address:
        description:
          - IPv4 address of the interface. Required unless O(state=deleted).
        type: str
      mask:
        description:
          - Subnet mask in dotted decimal format, for example V(255.255.255.0). Required for a VLAN interface.
        type: str
      type:
        description:
          - Kind of device the interface is bound to. Only VLAN interfaces are supported.
        type: str
        choices:
          - vlan
      port_id:
        description:
          - ID of the VLAN the interface is bound to. Required for a VLAN interface.
        type: str
      vrf:
        description:
          - Name of the VRF the interface belongs to. The VRF must exist. Leave out for the default VRF.
        type: str
  running_config:
    description:
      - Text to convert into structured data. Only used with O(state=parsed).
      - Give the output of C(show configuration snapshot | grep "ip interface") from the switch.
    type: str
  state:
    description:
      - What the module does with the given configuration.
      - C(merged) adds the given configuration to the switch and changes only the attributes that are
        given.
      - C(replaced) makes each given entry match the task exactly. Attributes that are left out go back
        to their default value.
      - C(overridden) makes the whole resource match the task. Entries found on the switch that are not
        in the task are removed.
      - C(deleted) removes the given entries. Without O(config), every entry of this resource is removed.
      - C(gathered) reads the configuration from the switch and returns it as RV(gathered). Nothing is
        changed.
      - C(rendered) returns the commands for the given configuration as RV(rendered), without connecting
        to the switch.
      - C(parsed) converts the text given in O(running_config) into structured data, returned as RV(parsed),
        without connecting to the switch.
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - gathered
      - rendered
      - parsed
    default: merged
"""

EXAMPLES = r"""
- name: Create a VLAN interface, Loopback0 and an interface in a VRF
  ale.aos8.aos8_l3_interfaces:
    config:
      - name: int_30
        address: 10.10.30.1
        mask: 255.255.255.0
        type: vlan
        port_id: '30'
      - name: Loopback0
        address: 10.255.0.1
      - name: int_31
        vrf: vrf-val
        address: 10.10.31.1
        mask: 255.255.255.0
        port_id: '31'
    state: merged

# Commands sent to the switch
# ---------------------------
# ip interface "int_30" address 10.10.30.1 mask 255.255.255.0 vlan 30
# ip interface "Loopback0" address 10.255.0.1
# vrf vrf-val ip interface "int_31" address 10.10.31.1 mask 255.255.255.0 vlan 31

- name: Change the address of an interface
  ale.aos8.aos8_l3_interfaces:
    config:
      - name: int_30
        address: 10.10.30.254
    state: merged

# Commands sent to the switch
# ---------------------------
# ip interface "int_30" address 10.10.30.254 mask 255.255.255.0 vlan 30

- name: Replace the configuration of an interface
  ale.aos8.aos8_l3_interfaces:
    config:
      - name: int_30
        address: 10.10.30.1
        mask: 255.255.255.0
        port_id: '30'
    state: replaced

# Commands sent to the switch
# ---------------------------
# ip interface "int_30" address 10.10.30.1 mask 255.255.255.0 vlan 30

- name: Read the IP interfaces from the switch
  ale.aos8.aos8_l3_interfaces:
    state: gathered

- name: Keep only these interfaces (every other VLAN interface and Loopback0 are removed)
  ale.aos8.aos8_l3_interfaces:
    config:
      - name: int_10
        address: 10.10.10.1
        mask: 255.255.255.0
        port_id: '10'
      - name: int_30
        address: 10.10.30.1
        mask: 255.255.255.0
        port_id: '30'
    state: overridden

# Commands sent to the switch (other entries found on the switch are removed in the same way)
# -------------------------------------------------------------------------------------------
# no ip interface "Loopback0"
# vrf vrf-val no ip interface "int_31"

- name: Show the commands for an interface without connecting to the switch
  ale.aos8.aos8_l3_interfaces:
    config:
      - name: int_40
        address: 10.10.40.1
        mask: 255.255.255.0
        port_id: '40'
    state: rendered

# Value returned as rendered
# --------------------------
# - ip interface "int_40" address 10.10.40.1 mask 255.255.255.0 vlan 40

- name: Convert configuration lines into structured data
  ale.aos8.aos8_l3_interfaces:
    running_config: |
      ip interface "Loopback0" address 10.255.0.1
      ip interface "int_10" address 10.10.10.1 mask 255.255.255.0 vlan 10 ifindex 1
      vrf vrf-val ip interface "int_99" address 10.10.99.1 mask 255.255.255.0 vlan 99 ifindex 3
    state: parsed

# Value returned as parsed
# ------------------------
# - name: Loopback0
#   address: 10.255.0.1
# - name: int_10
#   address: 10.10.10.1
#   mask: 255.255.255.0
#   type: vlan
#   port_id: '10'
# - name: int_99
#   vrf: vrf-val
#   address: 10.10.99.1
#   mask: 255.255.255.0
#   type: vlan
#   port_id: '99'

- name: Remove an interface
  ale.aos8.aos8_l3_interfaces:
    config:
      - name: int_30
    state: deleted

# Commands sent to the switch
# ---------------------------
# no ip interface "int_30"

- name: Remove every VLAN interface and Loopback0
  ale.aos8.aos8_l3_interfaces:
    state: deleted

# Commands sent to the switch (other entries found on the switch are removed in the same way)
# -------------------------------------------------------------------------------------------
# no ip interface "int_10"
"""

RETURN = r"""
---
before:
  description: The configuration found on the switch before the module ran.
  returned: when O(state) is C(merged) or C(replaced) or C(overridden) or C(deleted)
  type: list
  elements: dict
  sample: The configuration in the format of the O(config) option.
after:
  description: The configuration found on the switch after the module ran.
  returned: when the module changed the switch
  type: list
  elements: dict
  sample: The configuration in the format of the O(config) option.
commands:
  description: The commands sent to the switch. In check mode, the commands that would be sent.
  returned: when O(state) is C(merged) or C(replaced) or C(overridden) or C(deleted)
  type: list
  elements: str
  sample:
    - ip interface "int_30" address 10.10.30.1 mask 255.255.255.0 vlan 30
    - ip interface "Loopback0" address 10.255.0.1
    - vrf vrf-val ip interface "int_31" address 10.10.31.1 mask 255.255.255.0 vlan 31
gathered:
  description: The configuration read from the switch.
  returned: when O(state) is C(gathered)
  type: list
  elements: dict
  sample: The configuration in the format of the O(config) option.
parsed:
  description: The structured data built from O(running_config).
  returned: when O(state) is C(parsed)
  type: list
  elements: dict
  sample:
    - name: Loopback0
      address: 10.255.0.1
    - name: int_10
      address: 10.10.10.1
      mask: 255.255.255.0
      type: vlan
      port_id: '10'
    - name: int_99
      vrf: vrf-val
      address: 10.10.99.1
      mask: 255.255.255.0
      type: vlan
      port_id: '99'
rendered:
  description: The commands for the given configuration.
  returned: when O(state) is C(rendered)
  type: list
  elements: str
  sample:
    - ip interface "int_40" address 10.10.40.1 mask 255.255.255.0 vlan 40
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.l3_interfaces.l3_interfaces import (
    L3_interfacesArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.l3_interfaces.l3_interfaces import (
    L3_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=L3_interfacesArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = L3_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()

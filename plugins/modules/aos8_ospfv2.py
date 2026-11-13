#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_ospfv2
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_ospfv2
short_description: Resource module to configure OSPFv2
description:
  - This module manages the OSPFv2 global state, areas and interfaces of the default VRF on Alcatel-Lucent
    Enterprise OmniSwitch devices running AOS 8.
  - The module loads the OSPF software (C(ip load ospf)) when it is not loaded yet.
  - The OSPF configuration is one object, so C(replaced) and C(overridden) do the same thing.
version_added: 1.0.0
author:
  - Maxime Descloux (@MaximeALE)
  - Mathias Guillemot (@mathias-gt)
notes:
  - Tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.
  - This module works with connection C(ansible.netcommon.network_cli).
  - After a change, the configuration is saved to flash with C(write memory flash-synchro), unless C(ansible_aos_write_memory_flash)
    is set to C(false). Saving needs C(ansible_command_timeout) to be 60 seconds or more.
options:
  config:
    description:
      - The OSPFv2 configuration.
    type: dict
    suboptions:
      admin_state:
        description:
          - Administrative state of OSPF on the switch.
        type: str
        choices:
          - enable
          - disable
      areas:
        description:
          - A list of OSPF areas.
        type: list
        elements: dict
        suboptions:
          area_id:
            description:
              - ID of the area in dotted decimal format, for example V(0.0.0.0).
            type: str
            required: true
          interfaces:
            description:
              - IP interfaces that belong to the area.
            type: list
            elements: dict
            suboptions:
              interface:
                description:
                  - Name of the IP interface. The interface must exist.
                type: str
                required: true
              admin_state:
                description:
                  - Administrative state of OSPF on the interface. A new OSPF interface is disabled.
                type: str
                choices:
                  - enable
                  - disable
  running_config:
    description:
      - Text to convert into structured data. Only used with O(state=parsed).
      - Give the output of C(show configuration snapshot ospf) from the switch.
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
- name: Enable OSPF and put an interface in the backbone area
  ale.aos8.aos8_ospfv2:
    config:
      admin_state: enable
      areas:
        - area_id: 0.0.0.0
          interfaces:
            - interface: int_10
              admin_state: enable
    state: merged

# Commands sent to the switch (other entries found on the switch are removed in the same way)
# -------------------------------------------------------------------------------------------
# ip ospf area 0.0.0.0
# ip ospf interface "int_10"
# ip ospf interface "int_10" area 0.0.0.0
# ip ospf interface "int_10" admin-state enable
# ip ospf admin-state enable

- name: Disable OSPF on an interface
  ale.aos8.aos8_ospfv2:
    config:
      areas:
        - area_id: 0.0.0.0
          interfaces:
            - interface: int_10
              admin_state: disable
    state: merged

# Commands sent to the switch
# ---------------------------
# ip ospf interface "int_10" admin-state disable

- name: Move the interface to area 0.0.0.1 and remove area 0.0.0.0
  ale.aos8.aos8_ospfv2:
    config:
      admin_state: enable
      areas:
        - area_id: 0.0.0.1
          interfaces:
            - interface: int_10
              admin_state: enable
    state: replaced

# Commands sent to the switch
# ---------------------------
# ip ospf area 0.0.0.1
# ip ospf interface "int_10" area 0.0.0.1
# ip ospf interface "int_10" admin-state enable
# no ip ospf area 0.0.0.0

- name: Read the OSPF configuration from the switch
  ale.aos8.aos8_ospfv2:
    state: gathered

- name: Disable OSPF and keep only area 0.0.0.1, without interfaces
  ale.aos8.aos8_ospfv2:
    config:
      admin_state: disable
      areas:
        - area_id: 0.0.0.1
    state: overridden

# Commands sent to the switch
# ---------------------------
# ip ospf admin-state disable
# no ip ospf interface "int_10"

- name: Show the commands for an OSPF configuration without connecting to the switch
  ale.aos8.aos8_ospfv2:
    config:
      admin_state: enable
      areas:
        - area_id: 0.0.0.0
          interfaces:
            - interface: int_10
    state: rendered

# Value returned as rendered
# --------------------------
# - ip load ospf
# - ip ospf area 0.0.0.0
# - ip ospf interface "int_10"
# - ip ospf interface "int_10" area 0.0.0.0
# - ip ospf admin-state enable

- name: Convert configuration lines into structured data
  ale.aos8.aos8_ospfv2:
    running_config: |
      ip load ospf
      ip ospf area 0.0.0.0
      ip ospf interface "int_10"
      ip ospf interface "int_10" area 0.0.0.0
      ip ospf interface "int_10" admin-state enable
      ip ospf admin-state enable
    state: parsed

# Value returned as parsed
# ------------------------
# admin_state: enable
# areas:
#   - area_id: 0.0.0.0
#     interfaces:
#       - interface: int_10
#         admin_state: enable

- name: Disable OSPF and remove every area and interface
  ale.aos8.aos8_ospfv2:
    state: deleted

# Commands sent to the switch
# ---------------------------
# no ip ospf area 0.0.0.1
"""

RETURN = r"""
---
before:
  description: The configuration found on the switch before the module ran.
  returned: when O(state) is C(merged) or C(replaced) or C(overridden) or C(deleted)
  type: dict
  sample: The configuration in the format of the O(config) option.
after:
  description: The configuration found on the switch after the module ran.
  returned: when the module changed the switch
  type: dict
  sample: The configuration in the format of the O(config) option.
commands:
  description: The commands sent to the switch. In check mode, the commands that would be sent.
  returned: when O(state) is C(merged) or C(replaced) or C(overridden) or C(deleted)
  type: list
  elements: str
  sample:
    - ip ospf area 0.0.0.0
    - ip ospf interface "int_10"
    - ip ospf interface "int_10" area 0.0.0.0
    - ip ospf interface "int_10" admin-state enable
    - ip ospf admin-state enable
gathered:
  description: The configuration read from the switch.
  returned: when O(state) is C(gathered)
  type: dict
  sample: The configuration in the format of the O(config) option.
parsed:
  description: The structured data built from O(running_config).
  returned: when O(state) is C(parsed)
  type: dict
  sample:
    admin_state: enable
    areas:
      - area_id: 0.0.0.0
        interfaces:
          - interface: int_10
            admin_state: enable
rendered:
  description: The commands for the given configuration.
  returned: when O(state) is C(rendered)
  type: list
  elements: str
  sample:
    - ip load ospf
    - ip ospf area 0.0.0.0
    - ip ospf interface "int_10"
    - ip ospf interface "int_10" area 0.0.0.0
    - ip ospf admin-state enable
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.ospfv2.ospfv2 import (
    OspfV2_Args,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.ospfv2.ospfv2 import (
    Ospfv2,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=OspfV2_Args.argument_spec,
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

    result = Ospfv2(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()

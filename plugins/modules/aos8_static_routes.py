#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_static_routes
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_static_routes
short_description: Resource module to configure IPv4 static routes
description:
  - This module manages IPv4 static routes of the default VRF on Alcatel-Lucent Enterprise OmniSwitch
    devices running AOS 8.
  - The tag and name of an existing route cannot be changed in place. The module removes the route and
    creates it again when one of its attributes changes.
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
      - A list with one entry holding the static routes of the default VRF.
    type: list
    elements: dict
    suboptions:
      routes:
        description:
          - A list of static routes.
        type: list
        elements: dict
        suboptions:
          dest:
            description:
              - Destination of the route in C(network/prefix-length) format, for example V(172.31.1.0/24).
            type: str
            required: true
          next_hops:
            description:
              - Next hops of the route. With O(state=deleted), leave this out to remove every next hop
                of the destination.
            type: list
            elements: dict
            suboptions:
              forward_router_address:
                description:
                  - IPv4 address of the gateway. Give either this or O(config[].routes[].next_hops[].interface).
                type: str
              interface:
                description:
                  - Name of the IP interface the route points to.
                type: str
              admin_distance:
                description:
                  - Metric of the route. The switch default is 1.
                type: int
              tag:
                description:
                  - Tag of the route. Only for a route with O(config[].routes[].next_hops[].forward_router_address).
                type: int
              description:
                description:
                  - Name of the route. Only for a route with O(config[].routes[].next_hops[].forward_router_address).
                type: str
  running_config:
    description:
      - Text to convert into structured data. Only used with O(state=parsed).
      - Give the output of C(show configuration snapshot ip-routing) from the switch.
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
- name: Create static routes
  ale.aos8.aos8_static_routes:
    config:
      - routes:
          - dest: 172.31.1.0/24
            next_hops:
              - forward_router_address: 10.10.10.254
          - dest: 172.31.2.0/24
            next_hops:
              - forward_router_address: 10.10.10.254
                admin_distance: 5
                tag: 7
                description: Backup
          - dest: 172.31.3.0/24
            next_hops:
              - interface: int_10
    state: merged

# Commands sent to the switch
# ---------------------------
# ip static-route 172.31.1.0/24 gateway 10.10.10.254
# ip static-route 172.31.2.0/24 gateway 10.10.10.254 tag 7 name "Backup" metric 5
# ip static-route 172.31.3.0/24 interface "int_10"

- name: Replace the next hop of a destination
  ale.aos8.aos8_static_routes:
    config:
      - routes:
          - dest: 172.31.1.0/24
            next_hops:
              - forward_router_address: 10.10.10.253
    state: replaced

# Commands sent to the switch
# ---------------------------
# no ip static-route 172.31.1.0/24 gateway 10.10.10.254
# ip static-route 172.31.1.0/24 gateway 10.10.10.253

- name: Read the static routes from the switch
  ale.aos8.aos8_static_routes:
    state: gathered

- name: Keep only this route (every other static route is removed)
  ale.aos8.aos8_static_routes:
    config:
      - routes:
          - dest: 172.31.1.0/24
            next_hops:
              - forward_router_address: 10.10.10.253
    state: overridden

# Commands sent to the switch (other entries found on the switch are removed in the same way)
# -------------------------------------------------------------------------------------------
# no ip static-route 172.31.2.0/24 gateway 10.10.10.254
# no ip static-route 172.31.3.0/24 interface "int_10"

- name: Show the commands for a route without connecting to the switch
  ale.aos8.aos8_static_routes:
    config:
      - routes:
          - dest: 10.99.0.0/16
            next_hops:
              - forward_router_address: 10.10.10.254
                admin_distance: 10
    state: rendered

# Value returned as rendered
# --------------------------
# - ip static-route 10.99.0.0/16 gateway 10.10.10.254 metric 10

- name: Convert configuration lines into structured data
  ale.aos8.aos8_static_routes:
    running_config: |
      ip static-route 172.31.251.0/24 interface int_20 metric 1
      ip static-route 172.31.253.0/24 gateway 10.10.10.2 metric 1 tag 7 name "valroute"
    state: parsed

# Value returned as parsed
# ------------------------
# - routes:
#     - dest: 172.31.251.0/24
#       next_hops:
#         - interface: int_20
#           admin_distance: 1
#     - dest: 172.31.253.0/24
#       next_hops:
#         - forward_router_address: 10.10.10.2
#           admin_distance: 1
#           tag: 7
#           description: valroute

- name: Remove every next hop of a destination
  ale.aos8.aos8_static_routes:
    config:
      - routes:
          - dest: 172.31.1.0/24
    state: deleted

# Commands sent to the switch
# ---------------------------
# no ip static-route 172.31.1.0/24 gateway 10.10.10.253

- name: Remove every static route
  ale.aos8.aos8_static_routes:
    state: deleted

# Commands sent to the switch (other entries found on the switch are removed in the same way)
# -------------------------------------------------------------------------------------------
# no ip static-route 172.31.2.0/24 gateway 10.10.10.254
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
    - ip static-route 172.31.1.0/24 gateway 10.10.10.254
    - ip static-route 172.31.2.0/24 gateway 10.10.10.254 tag 7 name "Backup" metric 5
    - ip static-route 172.31.3.0/24 interface "int_10"
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
    - routes:
        - dest: 172.31.251.0/24
          next_hops:
            - interface: int_20
              admin_distance: 1
        - dest: 172.31.253.0/24
          next_hops:
            - forward_router_address: 10.10.10.2
              admin_distance: 1
              tag: 7
              description: valroute
rendered:
  description: The commands for the given configuration.
  returned: when O(state) is C(rendered)
  type: list
  elements: str
  sample:
    - ip static-route 10.99.0.0/16 gateway 10.10.10.254 metric 10
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.static_routes.static_routes import (
    Static_routesArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.static_routes.static_routes import (
    Static_routes,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Static_routesArgs.argument_spec,
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

    result = Static_routes(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()

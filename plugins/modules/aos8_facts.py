#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_facts
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_facts
short_description: Collect facts from AOS 8 devices
description:
  - Collects facts from an Alcatel-Lucent Enterprise OmniSwitch running AOS 8.
  - Basic facts about the switch are returned with the prefix C(ansible_net_).
  - The configuration handled by the resource modules is returned under C(ansible_network_resources).
version_added: 1.0.0
author:
  - Samuel Yip Kah Yean (@samuelyip74)
  - Mathias Guillemot (@mathias-gt)
notes:
  - Tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.
  - This module works with connection C(ansible.netcommon.network_cli).
options:
  gather_subset:
    description:
      - Selects the basic facts to collect.
      - V(min) and V(all) both collect the model, software version, system name and system description
        of the switch.
      - Give both V(!all) and V(!min) to collect no basic facts.
    type: list
    elements: str
    default:
      - min
  gather_network_resources:
    description:
      - Selects the resources whose configuration is collected.
      - V(all) collects every resource. The data of each resource has the format of the C(config) option
        of the resource module with the same name.
      - No resource is collected when this option is left out.
    type: list
    elements: str
    choices:
      - all
      - bgp
      - hostname
      - l2_interfaces
      - l3_interfaces
      - ntp
      - ospfv2
      - radius_servers
      - static_routes
      - switch_security
      - trap_managers
      - vlans
"""

EXAMPLES = r"""
- name: Collect the basic facts
  ale.aos8.aos8_facts:
    gather_subset: min

- name: Collect the VLANs and the system name, without basic facts
  ale.aos8.aos8_facts:
    gather_subset:
      - '!all'
      - '!min'
    gather_network_resources:
      - vlans
      - hostname

- name: Collect the basic facts and every resource
  ale.aos8.aos8_facts:
    gather_subset: all
    gather_network_resources: all

- name: Collect only the bgp resource
  ale.aos8.aos8_facts:
    gather_subset:
      - '!all'
      - '!min'
    gather_network_resources:
      - bgp

- name: Collect only the hostname resource
  ale.aos8.aos8_facts:
    gather_subset:
      - '!all'
      - '!min'
    gather_network_resources:
      - hostname

- name: Collect only the l2_interfaces resource
  ale.aos8.aos8_facts:
    gather_subset:
      - '!all'
      - '!min'
    gather_network_resources:
      - l2_interfaces

- name: Collect only the l3_interfaces resource
  ale.aos8.aos8_facts:
    gather_subset:
      - '!all'
      - '!min'
    gather_network_resources:
      - l3_interfaces

- name: Collect only the ntp resource
  ale.aos8.aos8_facts:
    gather_subset:
      - '!all'
      - '!min'
    gather_network_resources:
      - ntp

- name: Collect only the ospfv2 resource
  ale.aos8.aos8_facts:
    gather_subset:
      - '!all'
      - '!min'
    gather_network_resources:
      - ospfv2

- name: Collect only the radius_servers resource
  ale.aos8.aos8_facts:
    gather_subset:
      - '!all'
      - '!min'
    gather_network_resources:
      - radius_servers

- name: Collect only the static_routes resource
  ale.aos8.aos8_facts:
    gather_subset:
      - '!all'
      - '!min'
    gather_network_resources:
      - static_routes

- name: Collect only the switch_security resource
  ale.aos8.aos8_facts:
    gather_subset:
      - '!all'
      - '!min'
    gather_network_resources:
      - switch_security

- name: Collect only the trap_managers resource
  ale.aos8.aos8_facts:
    gather_subset:
      - '!all'
      - '!min'
    gather_network_resources:
      - trap_managers

- name: Collect only the vlans resource
  ale.aos8.aos8_facts:
    gather_subset:
      - '!all'
      - '!min'
    gather_network_resources:
      - vlans
"""

RETURN = r"""
---
ansible_net_model:
  description: Model of the switch.
  returned: when basic facts are collected
  type: str
  sample: OS687024-SIM
ansible_net_version:
  description: AOS release running on the switch.
  returned: when basic facts are collected
  type: str
  sample: 8.11.162.R01
ansible_net_hostname:
  description: System name of the switch.
  returned: when basic facts are collected
  type: str
  sample: val-os1
ansible_net_system:
  description: System description of the switch.
  returned: when basic facts are collected
  type: str
  sample: Alcatel-Lucent Enterprise OS687024-SIM 8.11.162.R01 GA, August 19, 2026.
ansible_net_network_os:
  description: Network operating system of the switch.
  returned: when basic facts are collected
  type: str
  sample: aos8
ansible_net_gather_subset:
  description: The basic fact subsets that were collected.
  returned: when basic facts are collected
  type: list
  elements: str
  sample:
    - default
ansible_net_gather_network_resources:
  description: The resources that were collected.
  returned: always
  type: list
  elements: str
  sample:
    - vlans
    - hostname
ansible_network_resources:
  description: The configuration of the collected resources, one key for each resource.
  returned: always
  type: dict
  sample:
    hostname:
      hostname: val-os1
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.facts.facts import (
    FactsArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.facts import Facts


def main():
    """
    Main entry point for module execution

    :returns: ansible_facts
    """
    module = AnsibleModule(argument_spec=FactsArgs.argument_spec, supports_check_mode=True)

    ansible_facts, warnings = Facts(module).get_facts()
    for warning in warnings:
        module.warn(warning)

    module.exit_json(ansible_facts=ansible_facts)


if __name__ == "__main__":
    main()

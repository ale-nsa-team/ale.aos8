.. _ale.aos8.aos8_facts_module:

ale.aos8.aos8_facts
*******************

**Collect facts from AOS 8 devices**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- Collects facts from an Alcatel-Lucent Enterprise OmniSwitch running AOS 8.
- Basic facts about the switch are returned with the prefix ``ansible_net_``.
- The configuration handled by the resource modules is returned under ``ansible_network_resources``.

Parameters
----------

.. list-table::
   :header-rows: 1
   :widths: 22 14 20 44

   * - Parameter
     - Type
     - Choices / default
     - Comments
   * - ``gather_network_resources``
     - list / elements=str
     - ``all``, ``bgp``, ``hostname``, ``l2_interfaces``, ``l3_interfaces``, ``ntp``, ``ospfv2``, ``radius_servers``, ``static_routes``, ``switch_security``, ``trap_managers``, ``vlans``
     - Selects the resources whose configuration is collected. ``all`` collects every resource. The data of each resource has the format of the ``config`` option of the resource module with the same name. No resource is collected when this option is left out.
   * - ``gather_subset``
     - list / elements=str
     - Default: ``["min"]``
     - Selects the basic facts to collect. ``min`` and ``all`` both collect the model, software version, system name and system description of the switch. Give both ``!all`` and ``!min`` to collect no basic facts.

Notes
-----

- Tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.
- This module works with connection ``ansible.netcommon.network_cli``.

Examples
--------

.. code-block:: yaml

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

Return values
-------------

.. list-table::
   :header-rows: 1
   :widths: 22 14 20 44

   * - Key
     - Type
     - Returned
     - Description
   * - ``ansible_net_gather_network_resources``
     - list
     - always
     - The resources that were collected. Sample: ``["vlans", "hostname"]``
   * - ``ansible_net_gather_subset``
     - list
     - when basic facts are collected
     - The basic fact subsets that were collected. Sample: ``["default"]``
   * - ``ansible_net_hostname``
     - str
     - when basic facts are collected
     - System name of the switch.
   * - ``ansible_net_model``
     - str
     - when basic facts are collected
     - Model of the switch.
   * - ``ansible_net_network_os``
     - str
     - when basic facts are collected
     - Network operating system of the switch.
   * - ``ansible_net_system``
     - str
     - when basic facts are collected
     - System description of the switch.
   * - ``ansible_net_version``
     - str
     - when basic facts are collected
     - AOS release running on the switch.
   * - ``ansible_network_resources``
     - dict
     - always
     - The configuration of the collected resources, one key for each resource. Sample: ``{"hostname": {"hostname": "val-os1"}}``

Authors
-------

- Samuel Yip Kah Yean (@samuelyip74)
- Mathias Guillemot (@mathias-gt)

.. _ale.aos8.aos8_bgp_module:

ale.aos8.aos8_bgp
*****************

**Resource module to configure BGP**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- This module manages the BGP autonomous system number, global state and neighbors of the default VRF on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
- The module loads the BGP software (``ip load bgp``) when it is not loaded yet.
- The BGP configuration is one object, so ``replaced`` and ``overridden`` do the same thing.
- The autonomous system number cannot be removed. ``deleted`` disables BGP and removes the neighbors.

Parameters
----------

.. list-table::
   :header-rows: 1
   :widths: 22 14 20 44

   * - Parameter
     - Type
     - Choices / default
     - Comments
   * - ``config``
     - dict
     -
     - The BGP configuration.
   * - – ``as_number``
     - str
     -
     - Autonomous system number of the switch.
   * - – ``bgp_admin_state``
     - str
     - ``enable``, ``disable``
     - Administrative state of BGP on the switch.
   * - – ``neighbor``
     - list / elements=dict
     -
     - A list of BGP neighbors.
   * - – – ``neighbor_address``
     - str / **required**
     -
     - IPv4 address of the neighbor. Aliases: peer
   * - – – ``neighbor_admin_state``
     - str
     - ``enable``, ``disable``
     - Administrative state of the neighbor. A new neighbor is disabled.
   * - – – ``remote_as``
     - str
     -
     - Autonomous system number of the neighbor.
   * - ``running_config``
     - str
     -
     - Text to convert into structured data. Only used with ``state=parsed``. Give the output of ``show configuration snapshot bgp`` from the switch.
   * - ``state``
     - str
     - ``merged`` (default), ``replaced``, ``overridden``, ``deleted``, ``gathered``, ``rendered``, ``parsed``
     - What the module does with the given configuration. ``merged`` adds the given configuration to the switch and changes only the attributes that are given. ``replaced`` makes each given entry match the task exactly. Attributes that are left out go back to their default value. ``overridden`` makes the whole resource match the task. Entries found on the switch that are not in the task are removed. ``deleted`` removes the given entries. Without ``config``, every entry of this resource is removed. ``gathered`` reads the configuration from the switch and returns it as ``gathered``. Nothing is changed. ``rendered`` returns the commands for the given configuration as ``rendered``, without connecting to the switch. ``parsed`` converts the text given in ``running_config`` into structured data, returned as ``parsed``, without connecting to the switch.

Notes
-----

- Tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.
- This module works with connection ``ansible.netcommon.network_cli``.
- After a change, the configuration is saved to flash with ``write memory flash-synchro``, unless ``ansible_aos_write_memory_flash`` is set to ``false``. Saving needs ``ansible_command_timeout`` to be 60 seconds or more.

Examples
--------

.. code-block:: yaml

    - name: Configure BGP with one neighbor
      ale.aos8.aos8_bgp:
        config:
          as_number: '65001'
          bgp_admin_state: enable
          neighbor:
            - neighbor_address: 10.10.10.254
              remote_as: '65002'
              neighbor_admin_state: enable
        state: merged

    # Commands sent to the switch (other entries found on the switch are removed in the same way)
    # -------------------------------------------------------------------------------------------
    # ip bgp neighbor 10.10.10.254
    # ip bgp neighbor 10.10.10.254 remote-as 65002
    # ip bgp neighbor 10.10.10.254 admin-state enable
    # ip bgp admin-state enable

    - name: Disable a neighbor (peer is an alias of neighbor_address)
      ale.aos8.aos8_bgp:
        config:
          neighbor:
            - peer: 10.10.10.254
              neighbor_admin_state: disable
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # ip bgp neighbor 10.10.10.254 admin-state disable

    - name: Replace the neighbors
      ale.aos8.aos8_bgp:
        config:
          as_number: '65001'
          bgp_admin_state: enable
          neighbor:
            - neighbor_address: 10.10.10.253
              remote_as: '65003'
        state: replaced

    # Commands sent to the switch
    # ---------------------------
    # no ip bgp neighbor 10.10.10.254
    # ip bgp neighbor 10.10.10.253
    # ip bgp neighbor 10.10.10.253 remote-as 65003

    - name: Read the BGP configuration from the switch
      ale.aos8.aos8_bgp:
        state: gathered

    - name: Disable BGP and keep the neighbor
      ale.aos8.aos8_bgp:
        config:
          as_number: '65001'
          bgp_admin_state: disable
          neighbor:
            - neighbor_address: 10.10.10.253
              remote_as: '65003'
        state: overridden

    # Commands sent to the switch
    # ---------------------------
    # ip bgp admin-state disable

    - name: Show the commands for a BGP configuration without connecting to the switch
      ale.aos8.aos8_bgp:
        config:
          as_number: '65010'
          bgp_admin_state: enable
        state: rendered

    # Value returned as rendered
    # --------------------------
    # - ip load bgp
    # - ip bgp autonomous-system 65010
    # - ip bgp admin-state enable

    - name: Convert configuration lines into structured data
      ale.aos8.aos8_bgp:
        running_config: |
          ip load bgp
          ip bgp autonomous-system 65001
          ip bgp neighbor 10.10.10.2
          ip bgp neighbor 10.10.10.2 remote-as 65002
          ip bgp neighbor 10.10.10.2 admin-state enable
          ip bgp admin-state enable
        state: parsed

    # Value returned as parsed
    # ------------------------
    # as_number: '65001'
    # bgp_admin_state: enable
    # neighbor:
    #   - neighbor_address: 10.10.10.2
    #     remote_as: '65002'
    #     neighbor_admin_state: enable

    - name: Remove every neighbor and disable BGP
      ale.aos8.aos8_bgp:
        state: deleted

    # Commands sent to the switch
    # ---------------------------
    # no ip bgp neighbor 10.10.10.253

Return values
-------------

.. list-table::
   :header-rows: 1
   :widths: 22 14 20 44

   * - Key
     - Type
     - Returned
     - Description
   * - ``after``
     - dict
     - when the module changed the switch
     - The configuration found on the switch after the module ran.
   * - ``before``
     - dict
     - when ``state`` is ``merged`` or ``replaced`` or ``overridden`` or ``deleted``
     - The configuration found on the switch before the module ran.
   * - ``commands``
     - list
     - when ``state`` is ``merged`` or ``replaced`` or ``overridden`` or ``deleted``
     - The commands sent to the switch. In check mode, the commands that would be sent. Sample: ``["ip bgp neighbor 10.10.10.254", "ip bgp neighbor 10.10.10.254 remote-as 65002", "ip bgp neighbor 10.10.10.254 admin-state enable", "ip bgp admin-state enable"]``
   * - ``gathered``
     - dict
     - when ``state`` is ``gathered``
     - The configuration read from the switch.
   * - ``parsed``
     - dict
     - when ``state`` is ``parsed``
     - The structured data built from ``running_config``. Sample: ``{"as_number": "65001", "bgp_admin_state": "enable", "neighbor": [{"neighbor_address": "10.10.10.2", "neighbor_admin_state": "enable", "remote_as": "65002"}]}``
   * - ``rendered``
     - list
     - when ``state`` is ``rendered``
     - The commands for the given configuration. Sample: ``["ip load bgp", "ip bgp autonomous-system 65010", "ip bgp admin-state enable"]``

Authors
-------

- Maxime Descloux (@MaximeALE)
- Mathias Guillemot (@mathias-gt)

.. _ale.aos8.aos8_vlans_module:

ale.aos8.aos8_vlans
*******************

**Resource module to configure VLANs**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- This module manages standard VLANs on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
- VLAN 1 is the default VLAN of the switch. It is never removed.

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
     - list / elements=dict
     -
     - A list of VLANs.
   * - – ``admin``
     - str
     - ``enable``, ``disable``
     - Administrative state of the VLAN. A new VLAN is created enabled.
   * - – ``mtu``
     - int
     -
     - Maximum IP packet size of the VLAN, in bytes. The switch default is 1500.
   * - – ``name``
     - str
     -
     - Description of the VLAN. The switch names a new VLAN ``VLAN <id>`` when no name is given.
   * - – ``operational_state``
     - str
     - ``enable``, ``disable``
     - Operational state of the VLAN. This value is read from the switch and returned by the module. It is ignored when given in a task.
   * - – ``vlan_id``
     - int / **required**
     -
     - ID of the VLAN.
   * - ``running_config``
     - str
     -
     - Text to convert into structured data. Only used with ``state=parsed``. Give the output of ``show vlan`` from the switch.
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

    - name: Create two VLANs
      ale.aos8.aos8_vlans:
        config:
          - vlan_id: 30
            name: Voice
            admin: enable
            mtu: 9000
          - vlan_id: 31
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # vlan 30 admin-state enable
    # vlan 30 name "Voice"
    # vlan 30 mtu-ip 9000
    # vlan 31 admin-state enable

    - name: Rename a VLAN and disable it
      ale.aos8.aos8_vlans:
        config:
          - vlan_id: 31
            name: Guest
            admin: disable
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # vlan 31 admin-state disable
    # vlan 31 name "Guest"

    - name: Replace the configuration of VLAN 30 (the MTU goes back to 1500)
      ale.aos8.aos8_vlans:
        config:
          - vlan_id: 30
            name: Voice
        state: replaced

    # Commands sent to the switch
    # ---------------------------
    # vlan 30 mtu-ip 1500

    - name: Read the VLANs from the switch
      ale.aos8.aos8_vlans:
        state: gathered

    - name: Keep only VLAN 10 and VLAN 30 (every other VLAN except VLAN 1 is removed)
      ale.aos8.aos8_vlans:
        config:
          - vlan_id: 10
            name: VAL-ISL
          - vlan_id: 30
            name: Voice
        state: overridden

    # Commands sent to the switch (other entries found on the switch are removed in the same way)
    # -------------------------------------------------------------------------------------------
    # no vlan 31

    - name: Show the commands for a VLAN without connecting to the switch
      ale.aos8.aos8_vlans:
        config:
          - vlan_id: 998
            name: Vlan 998
            admin: disable
        state: rendered

    # Value returned as rendered
    # --------------------------
    # - vlan 998 admin-state disable
    # - vlan 998 name "Vlan 998"

    - name: Convert the output of show vlan into structured data
      ale.aos8.aos8_vlans:
        running_config: |
          vlan    type   admin   oper    ip    mtu          name
          ------+-------+-------+------+------+------+------------------
          1      std       Ena     Ena   Dis    1500    VLAN 1
          20     std       Ena     Dis   Dis    1280    Users
        state: parsed

    # Value returned as parsed
    # ------------------------
    # - vlan_id: 1
    #   name: VLAN 1
    #   admin: enable
    #   mtu: 1500
    #   operational_state: enable
    # - vlan_id: 20
    #   name: Users
    #   admin: enable
    #   mtu: 1280
    #   operational_state: disable

    - name: Remove VLAN 30
      ale.aos8.aos8_vlans:
        config:
          - vlan_id: 30
        state: deleted

    # Commands sent to the switch
    # ---------------------------
    # no vlan 30

    - name: Remove every VLAN except VLAN 1
      ale.aos8.aos8_vlans:
        state: deleted

    # Commands sent to the switch (other entries found on the switch are removed in the same way)
    # -------------------------------------------------------------------------------------------
    # no vlan 10

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
     - list
     - when the module changed the switch
     - The configuration found on the switch after the module ran.
   * - ``before``
     - list
     - when ``state`` is ``merged`` or ``replaced`` or ``overridden`` or ``deleted``
     - The configuration found on the switch before the module ran.
   * - ``commands``
     - list
     - when ``state`` is ``merged`` or ``replaced`` or ``overridden`` or ``deleted``
     - The commands sent to the switch. In check mode, the commands that would be sent. Sample: ``["vlan 30 admin-state enable", "vlan 30 name \"Voice\"", "vlan 30 mtu-ip 9000", "vlan 31 admin-state enable"]``
   * - ``gathered``
     - list
     - when ``state`` is ``gathered``
     - The configuration read from the switch.
   * - ``parsed``
     - list
     - when ``state`` is ``parsed``
     - The structured data built from ``running_config``. Sample: ``[{"admin": "enable", "mtu": 1500, "name": "VLAN 1", "operational_state": "enable", "vlan_id": 1}, {"admin": "enable", "mtu": 1280, "name": "Users", "operational_state": "disable", "vlan_id": 20}]``
   * - ``rendered``
     - list
     - when ``state`` is ``rendered``
     - The commands for the given configuration. Sample: ``["vlan 998 admin-state disable", "vlan 998 name \"Vlan 998\""]``

Authors
-------

- Samuel Yip Kah Yean (@samuelyip74)
- Mathias Guillemot (@mathias-gt)

.. _ale.aos8.aos8_l2_interfaces_module:

ale.aos8.aos8_l2_interfaces
***************************

**Resource module to configure VLAN membership of ports and link aggregates**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- This module manages the VLAN port associations (VPA) of ports and link aggregates on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
- A port or link aggregate is an untagged member of one VLAN (its default VLAN) and can be a tagged member of other VLANs.
- Untagged membership of VLAN 1 is the factory default of every port. The module never removes it.

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
     - A list of VLAN memberships.
   * - – ``mode``
     - str
     - ``untagged``, ``tagged``
     - ``untagged`` makes the VLAN the default VLAN of the port. ``tagged`` adds the port to the VLAN with 802.1Q tagging. Required unless ``state=deleted``.
   * - – ``port_number``
     - str / **required**
     -
     - Port in ``chassis/slot/port`` format, for example ``1/1/5``, or ID of a link aggregate, for example ``5``.
   * - – ``port_type``
     - str
     - ``port``, ``linkagg``
     - Whether ``config[].port_number`` is a port or a link aggregate. The module works this out from the format of ``config[].port_number`` when it is left out.
   * - – ``vlan_id``
     - int / **required**
     -
     - ID of the VLAN. The VLAN must exist.
   * - ``running_config``
     - str
     -
     - Text to convert into structured data. Only used with ``state=parsed``. Give the output of ``show vlan members`` from the switch.
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

    - name: Add a port and a link aggregate to VLANs
      ale.aos8.aos8_l2_interfaces:
        config:
          - vlan_id: 30
            port_type: port
            port_number: 1/1/5
            mode: untagged
          - vlan_id: 31
            port_number: 1/1/5
            mode: tagged
          - vlan_id: 30
            port_type: linkagg
            port_number: '5'
            mode: tagged
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # vlan 30 members port 1/1/5 untagged
    # vlan 31 members port 1/1/5 tagged
    # vlan 30 members linkagg 5 tagged

    - name: Change link aggregate 5 from tagged to untagged in VLAN 30
      ale.aos8.aos8_l2_interfaces:
        config:
          - vlan_id: 30
            port_number: '5'
            mode: untagged
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # no vlan 30 members linkagg 5
    # vlan 30 members linkagg 5 untagged

    - name: Make port 1/1/6 a tagged member of VLAN 31
      ale.aos8.aos8_l2_interfaces:
        config:
          - vlan_id: 31
            port_number: 1/1/6
            mode: tagged
        state: replaced

    # Commands sent to the switch
    # ---------------------------
    # vlan 31 members port 1/1/6 tagged

    - name: Read the VLAN memberships from the switch
      ale.aos8.aos8_l2_interfaces:
        state: gathered

    - name: Keep only these memberships (every other one is removed, except untagged VLAN 1)
      ale.aos8.aos8_l2_interfaces:
        config:
          - vlan_id: 10
            port_number: 1/1/1
            mode: tagged
          - vlan_id: 30
            port_number: 1/1/5
            mode: untagged
        state: overridden

    # Commands sent to the switch (other entries found on the switch are removed in the same way)
    # -------------------------------------------------------------------------------------------
    # no vlan 31 members port 1/1/5
    # no vlan 31 members port 1/1/6
    # no vlan 30 members linkagg 5

    - name: Show the commands for a membership without connecting to the switch
      ale.aos8.aos8_l2_interfaces:
        config:
          - vlan_id: 30
            port_number: 1/1/7
            mode: untagged
        state: rendered

    # Value returned as rendered
    # --------------------------
    # - vlan 30 members port 1/1/7 untagged

    - name: Convert the output of show vlan members into structured data
      ale.aos8.aos8_l2_interfaces:
        running_config: |
          vlan       port         type         status
          --------+------------+------------+--------------
            1         1/1/1        untagged   forwarding
            99        0/5          tagged     inactive
        state: parsed

    # Value returned as parsed
    # ------------------------
    # - vlan_id: 1
    #   port_number: 1/1/1
    #   port_type: port
    #   mode: untagged
    # - vlan_id: 99
    #   port_number: '5'
    #   port_type: linkagg
    #   mode: tagged

    - name: Remove port 1/1/5 from VLAN 30
      ale.aos8.aos8_l2_interfaces:
        config:
          - vlan_id: 30
            port_number: 1/1/5
        state: deleted

    # Commands sent to the switch
    # ---------------------------
    # no vlan 30 members port 1/1/5

    - name: Remove every membership except untagged VLAN 1
      ale.aos8.aos8_l2_interfaces:
        state: deleted

    # Commands sent to the switch (other entries found on the switch are removed in the same way)
    # -------------------------------------------------------------------------------------------
    # no vlan 10 members port 1/1/1

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
     - The commands sent to the switch. In check mode, the commands that would be sent. Sample: ``["vlan 30 members port 1/1/5 untagged", "vlan 31 members port 1/1/5 tagged", "vlan 30 members linkagg 5 tagged"]``
   * - ``gathered``
     - list
     - when ``state`` is ``gathered``
     - The configuration read from the switch.
   * - ``parsed``
     - list
     - when ``state`` is ``parsed``
     - The structured data built from ``running_config``. Sample: ``[{"mode": "untagged", "port_number": "1/1/1", "port_type": "port", "vlan_id": 1}, {"mode": "tagged", "port_number": "5", "port_type": "linkagg", "vlan_id": 99}]``
   * - ``rendered``
     - list
     - when ``state`` is ``rendered``
     - The commands for the given configuration. Sample: ``["vlan 30 members port 1/1/7 untagged"]``

Authors
-------

- Samuel Yip Kah Yean (@samuelyip74)
- Mathias Guillemot (@mathias-gt)

.. _ale.aos8.aos8_l3_interfaces_module:

ale.aos8.aos8_l3_interfaces
***************************

**Resource module to configure IP interfaces**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- This module manages IPv4 interfaces bound to a VLAN, and Loopback0, on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
- Interfaces of other kinds (EMP, router ports, tunnels) are not read or changed by this module.

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
     - A list of IP interfaces.
   * - – ``address``
     - str
     -
     - IPv4 address of the interface. Required unless ``state=deleted``.
   * - – ``mask``
     - str
     -
     - Subnet mask in dotted decimal format, for example ``255.255.255.0``. Required for a VLAN interface.
   * - – ``name``
     - str / **required**
     -
     - Name of the IP interface. An interface whose name starts with ``Loopback`` only takes an address.
   * - – ``port_id``
     - str
     -
     - ID of the VLAN the interface is bound to. Required for a VLAN interface.
   * - – ``type``
     - str
     - ``vlan``
     - Kind of device the interface is bound to. Only VLAN interfaces are supported.
   * - – ``vrf``
     - str
     -
     - Name of the VRF the interface belongs to. The VRF must exist. Leave out for the default VRF.
   * - ``running_config``
     - str
     -
     - Text to convert into structured data. Only used with ``state=parsed``. Give the output of ``show configuration snapshot | grep "ip interface"`` from the switch.
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
     - The commands sent to the switch. In check mode, the commands that would be sent. Sample: ``["ip interface \"int_30\" address 10.10.30.1 mask 255.255.255.0 vlan 30", "ip interface \"Loopback0\" address 10.255.0.1", "vrf vrf-val ip interface \"int_31\" address 10.10.31.1 mask 255.255.255.0 vlan 31"]``
   * - ``gathered``
     - list
     - when ``state`` is ``gathered``
     - The configuration read from the switch.
   * - ``parsed``
     - list
     - when ``state`` is ``parsed``
     - The structured data built from ``running_config``. Sample: ``[{"address": "10.255.0.1", "name": "Loopback0"}, {"address": "10.10.10.1", "mask": "255.255.255.0", "name": "int_10", "port_id": "10", "type": "vlan"}, {"address": "10.10.99.1", "mask": "255.255.255.0", "name": "int_99", "port_id": "99", "type": "vlan", "vrf": "vrf-val"}]``
   * - ``rendered``
     - list
     - when ``state`` is ``rendered``
     - The commands for the given configuration. Sample: ``["ip interface \"int_40\" address 10.10.40.1 mask 255.255.255.0 vlan 40"]``

Authors
-------

- Samuel Yip Kah Yean (@samuelyip74)
- Mathias Guillemot (@mathias-gt)

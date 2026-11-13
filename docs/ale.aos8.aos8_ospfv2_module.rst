.. _ale.aos8.aos8_ospfv2_module:

ale.aos8.aos8_ospfv2
********************

**Resource module to configure OSPFv2**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- This module manages the OSPFv2 global state, areas and interfaces of the default VRF on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
- The module loads the OSPF software (``ip load ospf``) when it is not loaded yet.
- The OSPF configuration is one object, so ``replaced`` and ``overridden`` do the same thing.

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
     - The OSPFv2 configuration.
   * - – ``admin_state``
     - str
     - ``enable``, ``disable``
     - Administrative state of OSPF on the switch.
   * - – ``areas``
     - list / elements=dict
     -
     - A list of OSPF areas.
   * - – – ``area_id``
     - str / **required**
     -
     - ID of the area in dotted decimal format, for example ``0.0.0.0``.
   * - – – ``interfaces``
     - list / elements=dict
     -
     - IP interfaces that belong to the area.
   * - – – – ``admin_state``
     - str
     - ``enable``, ``disable``
     - Administrative state of OSPF on the interface. A new OSPF interface is disabled.
   * - – – – ``interface``
     - str / **required**
     -
     - Name of the IP interface. The interface must exist.
   * - ``running_config``
     - str
     -
     - Text to convert into structured data. Only used with ``state=parsed``. Give the output of ``show configuration snapshot ospf`` from the switch.
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
     - The commands sent to the switch. In check mode, the commands that would be sent. Sample: ``["ip ospf area 0.0.0.0", "ip ospf interface \"int_10\"", "ip ospf interface \"int_10\" area 0.0.0.0", "ip ospf interface \"int_10\" admin-state enable", "ip ospf admin-state enable"]``
   * - ``gathered``
     - dict
     - when ``state`` is ``gathered``
     - The configuration read from the switch.
   * - ``parsed``
     - dict
     - when ``state`` is ``parsed``
     - The structured data built from ``running_config``. Sample: ``{"admin_state": "enable", "areas": [{"area_id": "0.0.0.0", "interfaces": [{"admin_state": "enable", "interface": "int_10"}]}]}``
   * - ``rendered``
     - list
     - when ``state`` is ``rendered``
     - The commands for the given configuration. Sample: ``["ip load ospf", "ip ospf area 0.0.0.0", "ip ospf interface \"int_10\"", "ip ospf interface \"int_10\" area 0.0.0.0", "ip ospf admin-state enable"]``

Authors
-------

- Maxime Descloux (@MaximeALE)
- Mathias Guillemot (@mathias-gt)

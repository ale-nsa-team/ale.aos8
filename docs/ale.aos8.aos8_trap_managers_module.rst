.. _ale.aos8.aos8_trap_managers_module:

ale.aos8.aos8_trap_managers
***************************

**Resource module to configure SNMP trap stations**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- This module manages the SNMP stations that receive traps from Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.

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
     - A list of SNMP trap stations.
   * - – ``host``
     - str / **required**
     -
     - IP address of the station that receives the traps.
   * - – ``port``
     - int
     - Default: ``162``
     - UDP port the traps are sent to.
   * - – ``state``
     - str
     - ``enable`` (default), ``disable``
     - Whether traps are sent to the station.
   * - – ``string``
     - str
     - Default: ``public``
     - Name of the switch user account used to send the traps. The user must exist on the switch.
   * - – ``version``
     - str
     - ``v1``, ``v2`` (default), ``v3``
     - SNMP version of the traps. ``v3`` needs a user created with SNMP authentication and privacy, for example ``user <name> password <password> read-only all sha+aes priv-password <password>``.
   * - ``running_config``
     - str
     -
     - Text to convert into structured data. Only used with ``state=parsed``. Give the output of ``show configuration snapshot | grep "snmp station"`` from the switch.
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

    - name: Add SNMP trap stations
      ale.aos8.aos8_trap_managers:
        config:
          - host: 192.168.121.250
            string: snmpuser
            version: v2
            state: enable
          - host: 192.168.121.249
            port: 1162
            string: snmpuser
            version: v1
            state: disable
          - host: 192.168.121.248
            string: snmpv3user
            version: v3
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # snmp station 192.168.121.250 162 "snmpuser" v2 enable
    # snmp station 192.168.121.249 1162 "snmpuser" v1 disable
    # snmp station 192.168.121.248 162 "snmpv3user" v3 enable

    - name: Enable a station
      ale.aos8.aos8_trap_managers:
        config:
          - host: 192.168.121.249
            port: 1162
            string: snmpuser
            version: v1
            state: enable
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # snmp station 192.168.121.249 1162 "snmpuser" v1 enable

    - name: Replace a station (port and version go back to their defaults)
      ale.aos8.aos8_trap_managers:
        config:
          - host: 192.168.121.249
            string: snmpuser
        state: replaced

    # Commands sent to the switch
    # ---------------------------
    # snmp station 192.168.121.249 162 "snmpuser" v2 enable

    - name: Read the SNMP trap stations from the switch
      ale.aos8.aos8_trap_managers:
        state: gathered

    - name: Keep only one station (every other station is removed)
      ale.aos8.aos8_trap_managers:
        config:
          - host: 192.168.121.250
            string: snmpuser
        state: overridden

    # Commands sent to the switch (other entries found on the switch are removed in the same way)
    # -------------------------------------------------------------------------------------------
    # no snmp station 192.168.121.249
    # no snmp station 192.168.121.248

    - name: Show the commands for a station without connecting to the switch
      ale.aos8.aos8_trap_managers:
        config:
          - host: 10.0.0.9
            port: 1162
            string: ops
            version: v3
        state: rendered

    # Value returned as rendered
    # --------------------------
    # - snmp station 10.0.0.9 1162 "ops" v3 enable

    - name: Convert configuration lines into structured data
      ale.aos8.aos8_trap_managers:
        running_config: |
          snmp station 192.168.121.250 162 "valtest" v2 enable
          snmp station 192.168.121.249 162 "valtest" v1 disable
        state: parsed

    # Value returned as parsed
    # ------------------------
    # - host: 192.168.121.250
    #   port: 162
    #   string: valtest
    #   version: v2
    #   state: enable
    # - host: 192.168.121.249
    #   port: 162
    #   string: valtest
    #   version: v1
    #   state: disable

    - name: Remove a station
      ale.aos8.aos8_trap_managers:
        config:
          - host: 192.168.121.250
        state: deleted

    # Commands sent to the switch
    # ---------------------------
    # no snmp station 192.168.121.250

    - name: Remove every station
      ale.aos8.aos8_trap_managers:
        state: deleted

    # Commands sent to the switch
    # ---------------------------
    # no snmp station 192.168.121.249

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
     - The commands sent to the switch. In check mode, the commands that would be sent. Sample: ``["snmp station 192.168.121.250 162 \"snmpuser\" v2 enable", "snmp station 192.168.121.249 1162 \"snmpuser\" v1 disable", "snmp station 192.168.121.248 162 \"snmpv3user\" v3 enable"]``
   * - ``gathered``
     - list
     - when ``state`` is ``gathered``
     - The configuration read from the switch.
   * - ``parsed``
     - list
     - when ``state`` is ``parsed``
     - The structured data built from ``running_config``. Sample: ``[{"host": "192.168.121.250", "port": 162, "state": "enable", "string": "valtest", "version": "v2"}, {"host": "192.168.121.249", "port": 162, "state": "disable", "string": "valtest", "version": "v1"}]``
   * - ``rendered``
     - list
     - when ``state`` is ``rendered``
     - The commands for the given configuration. Sample: ``["snmp station 10.0.0.9 1162 \"ops\" v3 enable"]``

Authors
-------

- Samuel Yip Kah Yean (@samuelyip74)
- Mathias Guillemot (@mathias-gt)

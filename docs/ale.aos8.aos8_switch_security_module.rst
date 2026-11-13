.. _ale.aos8.aos8_switch_security_module:

ale.aos8.aos8_switch_security
*****************************

**Resource module to configure Authenticated Switch Access**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- This module sets which AAA server authenticates each management access method (console, Telnet, SSH, FTP, HTTP, SNMP) on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
- ``deleted`` sets an access method back to the servers of the ``default`` access method. The ``default`` access method itself is never reset.

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
     - A list of access methods.
   * - – ``aaa_servers_name``
     - str
     -
     - Name of the AAA server that authenticates the access method, or ``local`` for the local user database. Required unless ``state=deleted``.
   * - – ``access_method``
     - str / **required**
     - ``default``, ``console``, ``telnet``, ``ssh``, ``snmp``, ``http``, ``ftp``
     - Management access method. ``default`` applies to every method that has no setting of its own.
   * - ``running_config``
     - str
     -
     - Text to convert into structured data. Only used with ``state=parsed``. Give the output of ``show configuration snapshot | grep "aaa authentication"`` from the switch.
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

    - name: Authenticate Telnet, FTP and SNMP access with the local user database
      ale.aos8.aos8_switch_security:
        config:
          - access_method: telnet
            aaa_servers_name: local
          - access_method: ftp
            aaa_servers_name: local
          - access_method: snmp
            aaa_servers_name: local
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # aaa authentication telnet "local"
    # aaa authentication ftp "local"
    # aaa authentication snmp "local"

    - name: Set the server of HTTP access
      ale.aos8.aos8_switch_security:
        config:
          - access_method: http
            aaa_servers_name: local
        state: replaced

    # Commands sent to the switch
    # ---------------------------
    # aaa authentication http "local"

    - name: Read the access methods from the switch
      ale.aos8.aos8_switch_security:
        state: gathered

    - name: Set FTP access back to the default servers
      ale.aos8.aos8_switch_security:
        config:
          - access_method: ftp
        state: deleted

    # Commands sent to the switch
    # ---------------------------
    # aaa authentication ftp default

    - name: Keep only these access methods (every other one goes back to the default servers)
      ale.aos8.aos8_switch_security:
        config:
          - access_method: default
            aaa_servers_name: local
          - access_method: console
            aaa_servers_name: local
          - access_method: ssh
            aaa_servers_name: local
        state: overridden

    # Commands sent to the switch (other entries found on the switch are removed in the same way)
    # -------------------------------------------------------------------------------------------
    # aaa authentication telnet default
    # aaa authentication http default
    # aaa authentication snmp default

    - name: Show the commands for an access method without connecting to the switch
      ale.aos8.aos8_switch_security:
        config:
          - access_method: ssh
            aaa_servers_name: rad1
        state: rendered

    # Value returned as rendered
    # --------------------------
    # - aaa authentication ssh "rad1"

    - name: Convert configuration lines into structured data
      ale.aos8.aos8_switch_security:
        running_config: |
          aaa authentication default "local"
          aaa authentication console "local"
        state: parsed

    # Value returned as parsed
    # ------------------------
    # - access_method: default
    #   aaa_servers_name: local
    # - access_method: console
    #   aaa_servers_name: local

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
     - The commands sent to the switch. In check mode, the commands that would be sent. Sample: ``["aaa authentication telnet \"local\"", "aaa authentication ftp \"local\"", "aaa authentication snmp \"local\""]``
   * - ``gathered``
     - list
     - when ``state`` is ``gathered``
     - The configuration read from the switch.
   * - ``parsed``
     - list
     - when ``state`` is ``parsed``
     - The structured data built from ``running_config``. Sample: ``[{"aaa_servers_name": "local", "access_method": "default"}, {"aaa_servers_name": "local", "access_method": "console"}]``
   * - ``rendered``
     - list
     - when ``state`` is ``rendered``
     - The commands for the given configuration. Sample: ``["aaa authentication ssh \"rad1\""]``

Authors
-------

- Samuel Yip Kah Yean (@samuelyip74)
- Mathias Guillemot (@mathias-gt)

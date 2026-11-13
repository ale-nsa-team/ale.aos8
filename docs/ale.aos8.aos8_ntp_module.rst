.. _ale.aos8.aos8_ntp_module:

ale.aos8.aos8_ntp
*****************

**Resource module to configure NTP servers**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- This module manages the NTP servers on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
- The options of an existing server cannot be cleared in place. The module removes the server and creates it again when one of its options changes.
- The NTP configuration is one object, so ``replaced`` and ``overridden`` do the same thing.

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
     - The NTP configuration.
   * - – ``servers``
     - list / elements=dict
     -
     - A list of NTP servers.
   * - – – ``burst``
     - bool
     -
     - Sends a burst of packets at each poll interval when the server is reachable.
   * - – – ``iburst``
     - bool
     -
     - Sends a burst of packets when the server is unreachable, to speed up the first synchronization.
   * - – – ``maxpoll``
     - int
     -
     - Maximum poll interval, as a power of 2 in seconds. The switch default is 10 (1024 seconds).
   * - – – ``minpoll``
     - int
     -
     - Minimum poll interval, as a power of 2 in seconds. The switch default is 6 (64 seconds).
   * - – – ``prefer``
     - bool
     -
     - Marks the server as the preferred server.
   * - – – ``server``
     - str / **required**
     -
     - IP address or DNS name of the NTP server.
   * - – – ``version``
     - int
     - ``1``, ``2``, ``3``, ``4``
     - NTP version used with this server. The switch default is 4.
   * - ``running_config``
     - str
     -
     - Text to convert into structured data. Only used with ``state=parsed``. Give the output of ``show configuration snapshot ntp`` from the switch.
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

    - name: Add NTP servers
      ale.aos8.aos8_ntp:
        config:
          servers:
            - server: 192.168.121.250
            - server: 192.168.121.251
              prefer: true
            - server: 192.168.121.252
              minpoll: 4
              maxpoll: 12
              version: 3
            - server: 192.168.121.253
              burst: true
              iburst: true
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # ntp server 192.168.121.250
    # ntp server 192.168.121.251 prefer
    # ntp server 192.168.121.252 minpoll 4 maxpoll 12 version 3
    # ntp server 192.168.121.253 burst iburst

    - name: Set the NTP version of servers
      ale.aos8.aos8_ntp:
        config:
          servers:
            - server: 192.168.121.247
              version: 1
            - server: 192.168.121.248
              version: 2
            - server: 192.168.121.250
              version: 4
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # ntp server 192.168.121.247 version 1
    # ntp server 192.168.121.248 version 2

    - name: Keep two servers and clear the prefer option
      ale.aos8.aos8_ntp:
        config:
          servers:
            - server: 192.168.121.250
            - server: 192.168.121.251
        state: replaced

    # Commands sent to the switch
    # ---------------------------
    # no ntp server 192.168.121.247
    # no ntp server 192.168.121.248
    # no ntp server 192.168.121.252
    # no ntp server 192.168.121.253
    # no ntp server 192.168.121.251
    # ntp server 192.168.121.251

    - name: Read the NTP servers from the switch
      ale.aos8.aos8_ntp:
        state: gathered

    - name: Keep only one server
      ale.aos8.aos8_ntp:
        config:
          servers:
            - server: 192.168.121.250
        state: overridden

    # Commands sent to the switch
    # ---------------------------
    # no ntp server 192.168.121.251

    - name: Show the commands for an NTP server without connecting to the switch
      ale.aos8.aos8_ntp:
        config:
          servers:
            - server: 10.0.0.1
              prefer: true
        state: rendered

    # Value returned as rendered
    # --------------------------
    # - ntp server 10.0.0.1 prefer

    - name: Convert configuration lines into structured data
      ale.aos8.aos8_ntp:
        running_config: |
          ntp server 192.168.121.250
          ntp server 192.168.121.251 prefer
        state: parsed

    # Value returned as parsed
    # ------------------------
    # servers:
    #   - server: 192.168.121.250
    #   - server: 192.168.121.251
    #     prefer: true

    - name: Remove every NTP server
      ale.aos8.aos8_ntp:
        state: deleted

    # Commands sent to the switch
    # ---------------------------
    # no ntp server 192.168.121.250

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
     - The commands sent to the switch. In check mode, the commands that would be sent. Sample: ``["ntp server 192.168.121.250", "ntp server 192.168.121.251 prefer", "ntp server 192.168.121.252 minpoll 4 maxpoll 12 version 3", "ntp server 192.168.121.253 burst iburst"]``
   * - ``gathered``
     - dict
     - when ``state`` is ``gathered``
     - The configuration read from the switch.
   * - ``parsed``
     - dict
     - when ``state`` is ``parsed``
     - The structured data built from ``running_config``. Sample: ``{"servers": [{"server": "192.168.121.250"}, {"prefer": true, "server": "192.168.121.251"}]}``
   * - ``rendered``
     - list
     - when ``state`` is ``rendered``
     - The commands for the given configuration. Sample: ``["ntp server 10.0.0.1 prefer"]``

Authors
-------

- Maxime Descloux (@MaximeALE)
- Mathias Guillemot (@mathias-gt)

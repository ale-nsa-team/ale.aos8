.. _ale.aos8.aos8_radius_servers_module:

ale.aos8.aos8_radius_servers
****************************

**Resource module to configure RADIUS servers**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- This module manages RADIUS servers on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
- The switch stores the shared secret hashed, so the module cannot tell whether ``config[].key`` changed. The secret is only sent when the server is created or when another attribute changes.
- The shared secret is replaced by ``********`` in the ``commands`` and ``rendered`` returned by the module.
- Every RADIUS server of the switch must use the same VRF.

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
     - A list of RADIUS servers.
   * - – ``acct_port``
     - int
     - Default: ``1813``
     - UDP port for accounting requests.
   * - – ``auth_port``
     - int
     - Default: ``1812``
     - UDP port for authentication requests.
   * - – ``host``
     - str
     -
     - IP address or DNS name of the RADIUS server. Required unless ``state=deleted``.
   * - – ``key``
     - str
     -
     - Shared secret of the RADIUS server. Required when the server is created or changed.
   * - – ``name``
     - str / **required**
     -
     - Name of the RADIUS server on the switch.
   * - – ``retransmit``
     - int
     - Default: ``3``
     - Number of retries before the server is considered unreachable.
   * - – ``timeout``
     - int
     - Default: ``2``
     - Time in seconds the switch waits for an answer from the server.
   * - – ``vrf``
     - str
     - Default: ``default``
     - Name of the VRF used to reach the server. The VRF must exist, and every RADIUS server of the switch must use the same VRF.
   * - ``running_config``
     - str
     -
     - Text to convert into structured data. Only used with ``state=parsed``. Give the output of ``show configuration snapshot | grep "aaa radius-server"`` from the switch.
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

    - name: Create RADIUS servers
      ale.aos8.aos8_radius_servers:
        config:
          - name: rad1
            host: 192.168.121.251
            key: Secret123
          - name: rad2
            host: 192.168.121.252
            key: Secret123
            auth_port: 1645
            acct_port: 1646
            retransmit: 5
            timeout: 10
            vrf: default
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # aaa radius-server "rad1" host 192.168.121.251 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port 1813
    # aaa radius-server "rad2" host 192.168.121.252 key ******** retransmit 5 timeout 10 auth-port 1645 acct-port 1646

    - name: Change the timeout of a server
      ale.aos8.aos8_radius_servers:
        config:
          - name: rad1
            host: 192.168.121.251
            key: Secret123
            timeout: 5
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # aaa radius-server "rad1" host 192.168.121.251 key ******** retransmit 3 timeout 5 auth-port 1812 acct-port 1813

    - name: Replace a server (ports, retries and timeout go back to their defaults)
      ale.aos8.aos8_radius_servers:
        config:
          - name: rad2
            host: 192.168.121.252
            key: Secret123
        state: replaced

    # Commands sent to the switch
    # ---------------------------
    # aaa radius-server "rad2" host 192.168.121.252 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port 1813

    - name: Read the RADIUS servers from the switch
      ale.aos8.aos8_radius_servers:
        state: gathered

    - name: Keep only rad1 (every other RADIUS server is removed)
      ale.aos8.aos8_radius_servers:
        config:
          - name: rad1
            host: 192.168.121.251
            key: Secret123
            timeout: 5
        state: overridden

    # Commands sent to the switch
    # ---------------------------
    # no aaa radius-server "rad2"

    - name: Show the commands for a server without connecting to the switch
      ale.aos8.aos8_radius_servers:
        config:
          - name: rad9
            host: 10.0.0.9
            key: Secret123
        state: rendered

    # Value returned as rendered
    # --------------------------
    # - aaa radius-server "rad9" host 10.0.0.9 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port 1813

    - name: Convert configuration lines into structured data
      ale.aos8.aos8_radius_servers:
        running_config: |
          aaa radius-server "rad1" host 192.168.121.251 hash-key "25EA0FBE" retransmit 3 timeout 2 auth-port 1812 acct-port 1813 vrf-name default
        state: parsed

    # Value returned as parsed
    # ------------------------
    # - name: rad1
    #   host: 192.168.121.251
    #   retransmit: 3
    #   timeout: 2
    #   auth_port: 1812
    #   acct_port: 1813
    #   vrf: default

    - name: Remove a server
      ale.aos8.aos8_radius_servers:
        config:
          - name: rad1
        state: deleted

    # Commands sent to the switch
    # ---------------------------
    # no aaa radius-server "rad1"

    - name: Reach the RADIUS server through another VRF (no other server is configured)
      ale.aos8.aos8_radius_servers:
        config:
          - name: rad4
            host: 192.168.121.254
            key: Secret123
            vrf: vrf-val
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # aaa radius-server "rad4" host 192.168.121.254 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port 1813 vrf-name vrf-val

    - name: Remove every RADIUS server
      ale.aos8.aos8_radius_servers:
        state: deleted

    # Commands sent to the switch
    # ---------------------------
    # no aaa radius-server "rad4"

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
     - The commands sent to the switch. In check mode, the commands that would be sent. Sample: ``["aaa radius-server \"rad1\" host 192.168.121.251 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port 1813", "aaa radius-server \"rad2\" host 192.168.121.252 key ******** retransmit 5 timeout 10 auth-port 1645 acct-port 1646"]``
   * - ``gathered``
     - list
     - when ``state`` is ``gathered``
     - The configuration read from the switch.
   * - ``parsed``
     - list
     - when ``state`` is ``parsed``
     - The structured data built from ``running_config``. Sample: ``[{"acct_port": 1813, "auth_port": 1812, "host": "192.168.121.251", "name": "rad1", "retransmit": 3, "timeout": 2, "vrf": "default"}]``
   * - ``rendered``
     - list
     - when ``state`` is ``rendered``
     - The commands for the given configuration. Sample: ``["aaa radius-server \"rad9\" host 10.0.0.9 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port 1813"]``

Authors
-------

- Samuel Yip Kah Yean (@samuelyip74)
- Mathias Guillemot (@mathias-gt)

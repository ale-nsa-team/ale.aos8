.. _ale.aos8.aos8_static_routes_module:

ale.aos8.aos8_static_routes
***************************

**Resource module to configure IPv4 static routes**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- This module manages IPv4 static routes of the default VRF on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
- The tag and name of an existing route cannot be changed in place. The module removes the route and creates it again when one of its attributes changes.

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
     - A list with one entry holding the static routes of the default VRF.
   * - – ``routes``
     - list / elements=dict
     -
     - A list of static routes.
   * - – – ``dest``
     - str / **required**
     -
     - Destination of the route in ``network/prefix-length`` format, for example ``172.31.1.0/24``.
   * - – – ``next_hops``
     - list / elements=dict
     -
     - Next hops of the route. With ``state=deleted``, leave this out to remove every next hop of the destination.
   * - – – – ``admin_distance``
     - int
     -
     - Metric of the route. The switch default is 1.
   * - – – – ``description``
     - str
     -
     - Name of the route. Only for a route with ``config[].routes[].next_hops[].forward_router_address``.
   * - – – – ``forward_router_address``
     - str
     -
     - IPv4 address of the gateway. Give either this or ``config[].routes[].next_hops[].interface``.
   * - – – – ``interface``
     - str
     -
     - Name of the IP interface the route points to.
   * - – – – ``tag``
     - int
     -
     - Tag of the route. Only for a route with ``config[].routes[].next_hops[].forward_router_address``.
   * - ``running_config``
     - str
     -
     - Text to convert into structured data. Only used with ``state=parsed``. Give the output of ``show configuration snapshot ip-routing`` from the switch.
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

    - name: Create static routes
      ale.aos8.aos8_static_routes:
        config:
          - routes:
              - dest: 172.31.1.0/24
                next_hops:
                  - forward_router_address: 10.10.10.254
              - dest: 172.31.2.0/24
                next_hops:
                  - forward_router_address: 10.10.10.254
                    admin_distance: 5
                    tag: 7
                    description: Backup
              - dest: 172.31.3.0/24
                next_hops:
                  - interface: int_10
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # ip static-route 172.31.1.0/24 gateway 10.10.10.254
    # ip static-route 172.31.2.0/24 gateway 10.10.10.254 tag 7 name "Backup" metric 5
    # ip static-route 172.31.3.0/24 interface "int_10"

    - name: Replace the next hop of a destination
      ale.aos8.aos8_static_routes:
        config:
          - routes:
              - dest: 172.31.1.0/24
                next_hops:
                  - forward_router_address: 10.10.10.253
        state: replaced

    # Commands sent to the switch
    # ---------------------------
    # no ip static-route 172.31.1.0/24 gateway 10.10.10.254
    # ip static-route 172.31.1.0/24 gateway 10.10.10.253

    - name: Read the static routes from the switch
      ale.aos8.aos8_static_routes:
        state: gathered

    - name: Keep only this route (every other static route is removed)
      ale.aos8.aos8_static_routes:
        config:
          - routes:
              - dest: 172.31.1.0/24
                next_hops:
                  - forward_router_address: 10.10.10.253
        state: overridden

    # Commands sent to the switch (other entries found on the switch are removed in the same way)
    # -------------------------------------------------------------------------------------------
    # no ip static-route 172.31.2.0/24 gateway 10.10.10.254
    # no ip static-route 172.31.3.0/24 interface "int_10"

    - name: Show the commands for a route without connecting to the switch
      ale.aos8.aos8_static_routes:
        config:
          - routes:
              - dest: 10.99.0.0/16
                next_hops:
                  - forward_router_address: 10.10.10.254
                    admin_distance: 10
        state: rendered

    # Value returned as rendered
    # --------------------------
    # - ip static-route 10.99.0.0/16 gateway 10.10.10.254 metric 10

    - name: Convert configuration lines into structured data
      ale.aos8.aos8_static_routes:
        running_config: |
          ip static-route 172.31.251.0/24 interface int_20 metric 1
          ip static-route 172.31.253.0/24 gateway 10.10.10.2 metric 1 tag 7 name "valroute"
        state: parsed

    # Value returned as parsed
    # ------------------------
    # - routes:
    #     - dest: 172.31.251.0/24
    #       next_hops:
    #         - interface: int_20
    #           admin_distance: 1
    #     - dest: 172.31.253.0/24
    #       next_hops:
    #         - forward_router_address: 10.10.10.2
    #           admin_distance: 1
    #           tag: 7
    #           description: valroute

    - name: Remove every next hop of a destination
      ale.aos8.aos8_static_routes:
        config:
          - routes:
              - dest: 172.31.1.0/24
        state: deleted

    # Commands sent to the switch
    # ---------------------------
    # no ip static-route 172.31.1.0/24 gateway 10.10.10.253

    - name: Remove every static route
      ale.aos8.aos8_static_routes:
        state: deleted

    # Commands sent to the switch (other entries found on the switch are removed in the same way)
    # -------------------------------------------------------------------------------------------
    # no ip static-route 172.31.2.0/24 gateway 10.10.10.254

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
     - The commands sent to the switch. In check mode, the commands that would be sent. Sample: ``["ip static-route 172.31.1.0/24 gateway 10.10.10.254", "ip static-route 172.31.2.0/24 gateway 10.10.10.254 tag 7 name \"Backup\" metric 5", "ip static-route 172.31.3.0/24 interface \"int_10\""]``
   * - ``gathered``
     - list
     - when ``state`` is ``gathered``
     - The configuration read from the switch.
   * - ``parsed``
     - list
     - when ``state`` is ``parsed``
     - The structured data built from ``running_config``. Sample: ``[{"routes": [{"dest": "172.31.251.0/24", "next_hops": [{"admin_distance": 1, "interface": "int_20"}]}, {"dest": "172.31.253.0/24", "next_hops": [{"admin_distance": 1, "description": "valroute", "forward_router_address": "10.10.10.2", "tag": 7}]}]}]``
   * - ``rendered``
     - list
     - when ``state`` is ``rendered``
     - The commands for the given configuration. Sample: ``["ip static-route 10.99.0.0/16 gateway 10.10.10.254 metric 10"]``

Authors
-------

- Maxime Descloux (@MaximeALE)
- Mathias Guillemot (@mathias-gt)

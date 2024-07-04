# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Ntp_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


def _tmplt_ntp_servers(config_data):
    el = config_data["servers"]
    command = "ntp server"
    if el.get("server"):
        command += " {server}".format(**el)
    return command


class Ntp_Template(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Ntp_Template, self).__init__(
            lines=lines,
            tmplt=self,
            module=module,
        )
    # fmt: off
    PARSERS = [

        {
            "name": "servers",
            "getval": re.compile(
                r"""
                \s*ntp\sserver
                \s*(?P<host>\S+)*
                $""",
                re.VERBOSE,
            ),
            
            "setval": _tmplt_ntp_servers,
            "result": {
                "servers": {
                    "{{ host }}": {
                        "server": "{{ host }}",
                    },
                },
            },
        },
    ]
    # fmt: on
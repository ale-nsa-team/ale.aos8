#
# (c) 2016 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import json
import re

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils._text import to_bytes, to_text
from ansible.utils.display import Display
from ansible_collections.ansible.netcommon.plugins.plugin_utils.terminal_base import TerminalBase

display = Display()

class TerminalModule(TerminalBase):
    terminal_stdout_re = [re.compile(rb"[\r\n]?[\w\+\-\.:\/\[\]]+(?:\([^\)]+\)){0,3}(?:[>#]) ?$")]

    """
        List down all the known error messages from the device.
    """
    terminal_stderr_re = [
        re.compile(rb"ERROR: Invalid entry:", re.I),                                                        # AOS8
        re.compile(rb"ERROR: Allowed range of values for mtu is 1280 - 9198", re.I),                        # AOS8
        re.compile(rb"ERROR: VLAN", re.I),                                                                  # AOS8
        re.compile(rb"ERROR: A VPA already exists for given vlan and port", re.I),                          # AOS8
        re.compile(rb"ERROR: IP address format is w.x.y.z where w,x,y,z range is from 0 to 255", re.I),     # AOS8
        re.compile(rb"WARNING: Vlan \d+ does not currently exit", re.I),                                    # AOS8
        re.compile(rb"ERROR: Ip Address must not conflict with interface", re.I),                                    # AOS8
        re.compile(rb"% ?Error"),
        # re.compile(rb"^% \w+", re.M),
        re.compile(rb"% ?Bad secret"),
        re.compile(rb"[\r\n%] Bad passwords"),
        re.compile(rb"(?:incomplete|ambiguous) command", re.I),
        re.compile(rb"connection timed out", re.I),
        re.compile(rb"[^\r\n]+ not found"),
        re.compile(rb"'[^']' +returned error code: ?\d+"),
        re.compile(rb"Bad mask", re.I),
        re.compile(rb"% ?(\S+) ?overlaps with ?(\S+)", re.I),
        re.compile(rb"% ?(\S+) ?Error: ?[\s]+", re.I),
        re.compile(rb"% ?(\S+) ?Informational: ?[\s]+", re.I),
        re.compile(rb"Command authorization failed"),
        re.compile(rb"Command Rejected: ?[\s]+", re.I),
        re.compile(rb"% General session commands not allowed under the address family", re.I),
        re.compile(rb"% BGP: Error initializing topology", re.I),
        re.compile(rb"%SNMP agent not enabled", re.I),
        re.compile(rb"% Invalid", re.I),
    ]

    terminal_config_prompt = re.compile(r"^.+[>#\$]$")


    def on_open_shell(self):
        prompt = self._get_prompt()
        if prompt is None:
            return

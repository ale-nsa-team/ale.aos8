# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8_hostname config class
"""

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.base import (
    Aos8ResourceBase,
    quote,
)


class Hostname(Aos8ResourceBase):
    """The aos8_hostname config class"""

    RESOURCE = "hostname"

    def flatten(self, config):
        return [dict(config)] if config and config.get("hostname") else []

    def item_key(self, item):
        return "hostname"

    def is_protected(self, item):
        # AOS has no command to remove the system name
        return True

    def set_commands(self, want, have):
        return ["system name %s" % quote(want["hostname"])]

    def delete_commands(self, have):
        return []

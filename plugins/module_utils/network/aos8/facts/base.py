# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type


from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils


class Aos8FactsBase(object):
    """Base class for the aos8 resource facts.

    A subclass sets RESOURCE, ARGSPEC and COMMAND and implements parse(),
    which turns the device output into the ``config`` structure of the module.
    """

    RESOURCE = None
    ARGSPEC = None
    COMMAND = None

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = self.ARGSPEC.argument_spec

    def get_device_data(self, connection):
        return connection.get(self.COMMAND)

    def parse(self, data):
        raise NotImplementedError

    def _empty(self):
        return [] if self.argument_spec["config"]["type"] == "list" else {}

    def populate_facts(self, connection, ansible_facts, data=None):
        if data is None:
            data = self.get_device_data(connection)

        objs = self.parse(data or "")
        facts = self._empty()
        if objs:
            params = utils.validate_config(self.argument_spec, {"config": deepcopy(objs)})
            if isinstance(params["config"], list):
                facts = [utils.remove_empties(cfg) for cfg in params["config"]]
            else:
                facts = utils.remove_empties(params["config"])

        ansible_facts["ansible_network_resources"].pop(self.RESOURCE, None)
        ansible_facts["ansible_network_resources"][self.RESOURCE] = facts
        return ansible_facts

# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type


from collections import OrderedDict

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base import (
    ConfigBase,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    remove_empties,
)

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.facts import Facts


def quote(value):
    """Quote a free-text value the way AOS shows it in the configuration snapshot."""
    return '"%s"' % str(value).strip('"')


class Aos8ResourceBase(ConfigBase):
    """Common engine for the aos8 resource modules.

    The configuration of a resource is handled as a flat list of items.
    A subclass describes one item: its key, how to create or change it and
    how to remove it. The engine compares the wanted items with the items found
    on the switch and builds the command list for each state.
    """

    RESOURCE = None
    gather_subset = ["!all", "!min"]
    # values applied to attributes left out when state is replaced or overridden
    REPLACE_DEFAULTS = {}
    # send the removals before the additions
    DELETE_FIRST = True

    def __init__(self, module):
        super(Aos8ResourceBase, self).__init__(module)
        self.gather_network_resources = [self.RESOURCE]

    # ---- hooks -----------------------------------------------------------------
    def flatten(self, config):
        """Turn the module ``config`` structure into a list of items."""
        return [remove_empties(item) for item in config or []]

    def normalize(self, item):
        return item

    def item_key(self, item):
        raise NotImplementedError

    def item_scope(self, item):
        """Items sharing a scope are replaced together when state is replaced."""
        return self.item_key(item)

    def comparable(self, item):
        return dict((k, v) for k, v in item.items() if v is not None)

    def is_protected(self, item):
        """Protected items are never removed by the overridden and deleted states."""
        return False

    def order(self, item):
        return 0

    def validate(self, item):
        pass

    def matches_delete(self, want, have):
        return self.item_key(want) == self.item_key(have)

    def set_commands(self, want, have):
        raise NotImplementedError

    def delete_commands(self, have):
        raise NotImplementedError

    def finalize(self, commands, want, have):
        return commands

    def display(self, commands):
        """The commands as returned to the user (secrets hidden)."""
        return commands

    # ---- engine ----------------------------------------------------------------
    def get_facts(self, data=None):
        facts, _warnings = Facts(self._module).get_facts(
            self.gather_subset,
            self.gather_network_resources,
            data=data,
        )
        return facts["ansible_network_resources"].get(self.RESOURCE)

    def _items(self, config):
        if isinstance(config, dict):
            config = remove_empties(config)
        return [self.normalize(item) for item in self.flatten(config)]

    def execute_module(self):
        result = {"changed": False}
        state = self.state
        config = self._module.params.get("config")

        if state == "gathered":
            result["gathered"] = self.get_facts()
            return result

        if state == "parsed":
            running_config = self._module.params.get("running_config")
            if not running_config:
                self._module.fail_json(
                    msg="value of running_config parameter must not be empty for state parsed",
                )
            result["parsed"] = self.get_facts(data=running_config)
            return result

        if state in ("merged", "replaced", "overridden", "rendered") and not config:
            self._module.fail_json(
                msg="value of config parameter must not be empty for state {0}".format(state),
            )

        want = self._items(config) if config else []

        if state == "rendered":
            result["rendered"] = self.display(self.build_commands("merged", want, []))
            return result

        before = self.get_facts()
        commands = self.build_commands(state, want, self._items(before))
        result["before"] = before
        result["commands"] = self.display(commands)
        if commands:
            result["changed"] = True
            if not self._module.check_mode:
                self._connection.edit_config(commands)
                result["after"] = self.get_facts()
        return result

    def build_commands(self, state, want, have):
        have_map = OrderedDict((self.item_key(item), item) for item in have)
        want_map = OrderedDict((self.item_key(item), item) for item in want)
        to_set = []
        to_delete = []

        if state in ("merged", "replaced", "overridden"):
            for key, item in want_map.items():
                current = have_map.get(key)
                if state == "merged" and current:
                    item = dict(current, **item)
                elif state != "merged":
                    item = dict(self.REPLACE_DEFAULTS, **item)
                self.validate(item)
                if current is None or self.comparable(item) != self.comparable(current):
                    to_set.append((item, current))

            if state == "replaced":
                scopes = [self.item_scope(item) for item in want]
                to_delete = [
                    item
                    for key, item in have_map.items()
                    if key not in want_map and self.item_scope(item) in scopes
                ]
            elif state == "overridden":
                to_delete = [item for key, item in have_map.items() if key not in want_map]

        elif state == "deleted":
            if want:
                to_delete = [
                    item for item in have if any(self.matches_delete(w, item) for w in want)
                ]
            else:
                to_delete = list(have)

        to_delete = [item for item in to_delete if not self.is_protected(item)]

        removals = []
        for item in sorted(to_delete, key=self.order, reverse=True):
            removals.extend(self.delete_commands(item))
        additions = []
        for item, current in sorted(to_set, key=lambda pair: self.order(pair[0])):
            additions.extend(self.set_commands(item, current))
        commands = removals + additions if self.DELETE_FIRST else additions + removals
        return self.finalize(commands, want, have)

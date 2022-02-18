#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=missing-module-docstring

from csv import DictReader
from typing import AnyStr

from ansible.module_utils.common.text.converters import to_text
from ansible.inventory.data import InventoryData
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible.utils.display import Display

DOCUMENTATION = """
    name: inventory_csv
    plugin_type: inventory
    short_description: Use a CSV file as an inventory source
    author: "David Drugeon-Hamon"
    description:
        - Use a CSV file as an inventory source extends_documentation_fragment:
        - constructed
    options:
        plugin:
            description: token that ensures this is a source file for the 'csv' plugin
            required: True
            choices: ['csv']
"""

EXAMPLES = """
# sample CSV file
# host,groups
# web1,webservers zone1
# web2,webservers zone2
# db1,dbservers zone1
# db2,dbservers zone2
"""

display = Display()


class InventoryModule(BaseInventoryPlugin, Constructable):
    """Main entrypoint for Ansible Inventory Plugin."""

    NAME = "inventory_csv"

    def verify_file(self, path: AnyStr) -> bool:
        """
        Verify that this is a valid file to consume.
        If the file does not exist or does not end with the correct string,
        then Ansible will raise an error.

        Parameters
        ----------
        path : AnyStr
            The path to the file to verify.

        Returns
        -------
        bool
            True if the file is valid, otherwise False.
        """
        valid = False
        _path: str = to_text(path)
        valid_files = ("inventory_csv.yaml", "inventory_csv.yml")

        if super().verify_file(_path):
            # base class verifies that file exists and is readable by current user
            if _path.endswith(valid_files):
                valid = True
        return valid

    def _populate(self, csv_data: DictReader) -> None:
        """Populate the inventory from the CSV file."""
        raise NotImplementedError("_populate not implemented")

    def parse(
        self,
        inventory: InventoryData,
        loader: DataLoader,
        path: AnyStr,
        cache: bool = True,
    ) -> None:
        """Parse the inventory file."""
        super().parse(inventory, loader, path, cache)

        display.vvv("Reading configuration data from: %s" % to_text(path))
        config = self._read_config_data(path)
        self.groups = self.get_option("groups")
        self.keyed_groups = self.get_option("keyed_groups")

        with open(config["source"], "r") as csv_file:
            csv_data = DictReader(csv_file)
            self._populate(csv_data)

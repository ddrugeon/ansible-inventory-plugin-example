from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.inventory.data import InventoryData

import csv

DOCUMENTATION = """
    name: csv
    plugin_type: inventory
    short_description: Use a CSV file as an inventory source
    description:
        - Use a CSV file as an inventory source
    extends_documentation_fragment:
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


class InventoryModule(BaseInventoryPlugin):

    NAME = "csv"

    def verify_file(self, path):
        """return true/false if this is possibly a valid file for this plugin to consume"""
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current user
            if path.endswith((f"{self.NAME}.yml", f"{self.NAME}.yaml")):
                valid = True
        return valid

    def parse(self, inventory: InventoryData, loader, path: str, cache: bool = True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        config = self._read_config_data(path)
        input_data = csv.DictReader(open(config["source"]))
        for entry in input_data:
            host = entry["host"]
            groups = entry["groups"].split(",")
            inventory.add_group(groups)
            inventory.add_host(host, groups)

from ansible.plugins.inventory import BaseInventoryPlugin

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


class InventoryModule(BaseInventoryPlugin):

    NAME = "csv"

    def verify_file(self, path):
        """return true/false if this is possibly a valid file for this plugin to consume"""
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current user
            if path.endswith(("csv.yaml", "csv.yml")):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)

# License AGPL-3.0 or Later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Test Task Packed Picking',
    'version': '16.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Module for creating packed pickings via wizard in inventory',
    'description': """
        This module provides functionality to create packed pickings using a custom wizard in Odoo Inventory.

        Features:
        - Allows creation of pickings with custom packaging directly from a wizard.
        - Supports setting quantities, serial numbers, and custom package names.
        - Enables setting pickings to 'Ready' state with minimal steps.

        Technical Details:
        - Developed following OCA guidelines.
        - Includes testing for core functionality.
        - Linted and formatted per OCA standards.
    """,
    'author': 'Dmitry Meita',
    'license': 'AGPL-3',
    'website': 'https://github.com/tendil/odoo_packed_picking_module',
    'depends': [
        'base',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizards/packed_picking_wizard_views.xml',
    ],
    'demo': [
    ],
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'maintainers': ['tendil'],
    'repository': 'https://github.com/tendil/odoo_packed_picking_module',
    'installable': True,
    'application': False,
    'auto_install': False,
    'development_status': 'Beta',
}

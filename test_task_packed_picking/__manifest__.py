# License AGPL-3.0 or Later (http://www.gnu.org/licenses/agpl).
{
    "name": "Test Task Packed Picking",
    "version": "16.0.1.0.0",
    "category": "Inventory",
    "summary": "Module for creating packed pickings via wizard in inventory",
    "author": "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/tendil/test_task_packed_picking",
    "depends": [
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/packed_picking_wizard_views.xml",
    ],
    "maintainers": ["tendil"],
    "repository": "https://github.com/tendil/odoo_packed_picking_module",
    "installable": True,
    "application": False,
    "auto_install": False,
    "development_status": "Beta",
}

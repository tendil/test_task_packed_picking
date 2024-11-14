import logging

from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestPackedPicking(TransactionCase):
    def setUp(self):
        super(TestPackedPicking, self).setUp()
        # Create fixtures and test data
        self.operation_type = self.env.ref("stock.picking_type_out")
        self.owner = self.env.user.partner_id
        self.location = self.env.ref("stock.stock_location_stock")
        self.location_dest = self.env.ref("stock.stock_location_customers")
        self.product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
                "uom_id": self.env.ref("uom.product_uom_unit").id,
            }
        )

        # Ensure product availability in stock
        self.env["stock.quant"]._update_available_quantity(
            self.product, self.location, 100
        )
        _logger.info(
            f"Stock quantity for '{self.product.name}' updated in location: 100"
        )

    def test_create_packed_picking_basic(self):
        """Check basic scenario of creating a picking with product moves."""
        stock_move_data = [(self.product.id, 10, None)]
        picking = self.env["stock.picking"]._create_packed_picking(
            operation_type=self.operation_type,
            stock_move_data=stock_move_data,
            owner=self.owner,
            location=self.location,
            location_dest_id=self.location_dest,
            package_name="Test Package",
            create_lots=False,
            set_ready=True,
        )
        self.assertTrue(picking.exists(), "Picking was not created.")
        self.assertEqual(
            picking.picking_type_id, self.operation_type, "Incorrect operation type."
        )
        self.assertEqual(picking.state, "done", "Picking was not set to 'done' state.")
        _logger.info(f"Picking creation test passed for picking ID: {picking.id}")

    def test_access_error(self):
        """Check access errors."""
        # Create a temporary user with minimal permissions
        limited_user = self.env["res.users"].create(
            {"name": "Limited User", "login": "limited_user", "groups_id": [(6, 0, [])]}
        )

        with self.assertRaises(AccessError):
            # Perform action as limited user without `sudo`
            self.env["stock.picking"].with_user(limited_user).sudo(
                False
            )._create_packed_picking(
                operation_type=self.operation_type,
                stock_move_data=[(self.product.id, 5, None)],
                owner=limited_user.partner_id,
                location=self.location,
                location_dest_id=self.location_dest,
                set_ready=True,
            )
        _logger.info("AccessError was successfully handled.")

    def test_wizard_action_create_picking(self):
        """Test picking creation through wizard."""
        wizard = self.env["test.task.packed.picking.wizard"].create(
            {
                "operation_type_id": self.operation_type.id,
                "owner_id": self.owner.id,
                "location_id": self.location.id,
                "location_dest_id": self.location_dest.id,
                "package_name": "Test Package",
                "set_ready": True,
                "create_lots": True,
            }
        )

        # Add product lines
        wizard.line_ids.create(
            {
                "wizard_id": wizard.id,
                "product_id": self.product.id,
                "qty_done": 3,
                "serial": "SER456",
            }
        )

        action = wizard.action_create_picking()
        picking = self.env["stock.picking"].browse(action["res_id"])
        self.assertTrue(picking.exists(), "Picking was not created via wizard.")
        self.assertEqual(
            picking.package_level_ids.package_id.name,
            "Test Package",
            "Package name does not match.",
        )
        self.assertEqual(picking.state, "done", "Picking was not set to 'done' state.")
        _logger.info(f"Wizard successfully created picking with ID: {picking.id}")

    def test_notification_responsible_user(self):
        """Check responsible user notification."""
        user = self.env.ref("base.user_demo")
        wizard = self.env["test.task.packed.picking.wizard"].create(
            {
                "operation_type_id": self.operation_type.id,
                "responsible_user_id": user.id,
                "location_id": self.location.id,
                "location_dest_id": self.location_dest.id,
            }
        )

        # Add product lines in wizard to specify move quantities
        wizard.line_ids.create(
            {
                "wizard_id": wizard.id,
                "product_id": self.product.id,
                "qty_done": 5,  # Specify quantity for qty_done field
                "serial": "SER789",
            }
        )

        # Execute picking creation
        action = wizard.action_create_picking()
        picking = self.env["stock.picking"].browse(action["res_id"])

        # Check that the responsible user was notified
        self.assertIn(
            user.partner_id.id,
            picking.message_partner_ids.ids,
            "Responsible user was not notified.",
        )
        _logger.info(f"Responsible user ID {user.id} was successfully notified.")

from odoo.tests.common import TransactionCase


class TestPackedPickingImproved(TransactionCase):

    def setUp(self):
        super(TestPackedPickingImproved, self).setUp()
        self.picking_type = self.env.ref('stock.picking_type_out')
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
        })
        self.location_src = self.env.ref('stock.stock_location_stock')
        self.location_dest = self.env.ref('stock.stock_location_customers')

    def test_create_packed_picking_with_product(self):
        """Test the creation of a packed picking with a product move line."""
        stock_move_data = [(self.product.id, 5.0, None)]

        picking = self.env['stock.picking']._create_packed_picking(
            operation_type=self.picking_type,
            stock_move_data=stock_move_data,
            location=self.location_src,
            location_dest_id=self.location_dest,
        )

        self.assertTrue(picking, "Stock picking was not created.")
        self.assertEqual(picking.state, 'confirmed', "Stock picking state should be 'confirmed'.")

        self.assertEqual(len(picking.move_lines), 1, "Picking should have one move line.")
        move_line = picking.move_lines[0]
        self.assertEqual(move_line.product_id, self.product, "Product in move line should match the test product.")
        self.assertEqual(move_line.product_uom_qty, 5.0, "Product quantity in move line should be 5.0.")

"""
Module to enhance stock picking operations in Odoo by adding
custom packing and validation functionality.
"""

import logging

from odoo import _, api, exceptions, models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def _create_packed_picking(
        self,
        operation_type,
        stock_move_data,
        owner=None,
        location=None,
        location_dest_id=None,
        package_name=None,
        create_lots=False,
        set_ready=False,
    ):
        """Create a picking and put its product into a a package.
        This is equal to the following sequence:
            - Create a new picking
            - Assign an owner
            - Add products and set qty_done
            - Mark as "Todo"
            - Put in pack
        Args:
            operation_type (stock.picking.type): Operation type
            stock_move_data (List of tuples): [(product_id, qty_done, serial)]
                - (Integer) product_id: id of the product
                - (float) qty_done: quantity done
                - (Char, optional) serial: serial number to assign.
        Default lot names will be used if is None or == False
        Used only if 'create_lots==True'
        owner (res.partner, optional): Owner of the product
        location (stock.location, optional): Source location if differs from the
        operation type one
        location_dest (stock.location, optional): Destination location if differs
        from the operation type one
        package_name (Char, optional): Name to be assigned to the package. Default
        name will be used if not provided.
        set_ready (bool, optional): Try to set picking to the "Ready" state.
        Returns:
            stock.picking: Created picking
        """
        # Set default locations and owner if not provided
        location = location or operation_type.default_location_src_id
        location_dest_id = location_dest_id or operation_type.default_location_dest_id
        owner = owner or self.env.user.partner_id

        # Create the picking record
        picking_vals = {
            "picking_type_id": operation_type.id,
            "location_id": location.id,
            "location_dest_id": location_dest_id.id,
            "owner_id": owner.id,
        }
        stock_picking = self.env["stock.picking"].create(picking_vals)
        _logger.info(f"Created new picking with ID {stock_picking.id}")

        error_products = []

        # Process each product in the move data
        for product_id, qty_done, serial in stock_move_data:
            try:
                product = self.env["product.product"].browse(product_id)
                move_vals = {
                    "name": product.name,
                    "product_id": product.id,
                    "product_uom_qty": qty_done,
                    "product_uom": product.uom_id.id,
                    "location_id": location.id,
                    "location_dest_id": location_dest_id.id,
                    "picking_id": stock_picking.id,
                }
                if create_lots and serial:
                    move_vals["lot_ids"] = [
                        (0, 0, {"name": serial, "product_id": product.id})
                    ]

                # Create the stock move
                self.env["stock.move"].create(move_vals)
                _logger.info(
                    f"Added move for product {product.name} with quantity {qty_done}"
                )
            except exceptions.AccessError as e:
                _logger.error(f"Error adding move for product {product_id}: {e}")
                continue

        # If there were any access errors, raise a single error with details
        if error_products:
            raise exceptions.UserError(
                _(
                    f"Could not add moves for the following products due "
                    f"to access errors: {', '.join(map(str, error_products))}"
                )
            )

        # Confirm the picking and set quantities
        stock_picking.action_confirm()

        # Package handling
        if package_name:
            package = self.env["stock.quant.package"].create({"name": package_name})
            self.env["stock.package_level"].create(
                {
                    "package_id": package.id,
                    "picking_id": stock_picking.id,
                    "location_id": location.id,
                    "location_dest_id": location_dest_id.id,
                    "move_line_ids": [(6, 0, stock_picking.move_line_ids.ids)],
                    "company_id": stock_picking.company_id.id,
                }
            )
            _logger.info(
                f"Created package {package_name} for picking {stock_picking.id}"
            )

        if package_name:
            package = self.env["stock.quant.package"].create({"name": package_name})
            stock_picking.move_line_ids.write({"result_package_id": package.id})
            _logger.info(
                f"Created package {package_name} for picking {stock_picking.id}"
            )
        else:
            _logger.info(
                f"Package creation skipped for picking {stock_picking.id} "
                f"as no package_name was provided."
            )

        # Set to "Ready" state if required
        if set_ready:
            stock_picking.button_validate()
            _logger.info(f"Picking {stock_picking.id} validated and set to Ready.")

        return stock_picking

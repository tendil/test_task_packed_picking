"""
Module for managing the creation of packed pickings through a wizard,
including notifications for responsible users.
"""

import logging

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class TestTaskPackedPickingWizard(models.TransientModel):
    """Wizard to facilitate the creation of packed pickings with custom options."""

    _name = "test.task.packed.picking.wizard"
    _description = "Test Task Packed Picking Wizard"

    # Fields
    operation_type_id = fields.Many2one(
        comodel_name="stock.picking.type", required=True
    )
    create_lots = fields.Boolean(default=False)
    owner_id = fields.Many2one(
        comodel_name="res.partner",
    )
    location_id = fields.Many2one(
        comodel_name="stock.location", string="Source Location"
    )
    location_dest_id = fields.Many2one(
        comodel_name="stock.location", string="Destination Location"
    )
    package_name = fields.Char()
    set_ready = fields.Boolean(default=False)
    responsible_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible User",
        help="User to be notified when the picking is created.",
    )
    line_ids = fields.One2many(
        comodel_name="test.task.packed.picking.line.wizard",
        inverse_name="wizard_id",
        string="Lines",
    )

    def action_create_picking(self):
        """
        Action to create the picking and notify the responsible user.

        Collects line data, creates a picking, and sends a notification.
        """
        self.ensure_one()
        _logger.info(f"Starting action_create_picking for wizard ID: {self.ids}")

        # Prepare move data for picking creation
        stock_move_data = [
            (line.product_id.id, line.qty_done, line.serial) for line in self.line_ids
        ]

        try:
            # Create picking
            picking = self.env["stock.picking"]._create_packed_picking(
                operation_type=self.operation_type_id,
                stock_move_data=stock_move_data,
                owner=self.owner_id,
                location=self.location_id,
                location_dest_id=self.location_dest_id,
                package_name=self.package_name,
                create_lots=self.create_lots,
                set_ready=self.set_ready,
            )
            _logger.info(f"Picking created with ID: {picking.id}")

            # Notify responsible user if specified
            if self.responsible_user_id:
                self._notify_responsible_user(picking)

            # Return action to open the newly created picking
            return self._get_picking_action(picking.id)
        except Exception as e:
            _logger.error(f"Failed to create picking: {e}")
            raise ValueError(
                _(f"An error occurred while creating the picking: {e}")
            ) from e

    def _notify_responsible_user(self, picking):
        """
        Sends a notification to the responsible user, if defined.

        Args:
            picking (models.Model): The picking created by the wizard.
        """
        responsible_partner_id = self.responsible_user_id.partner_id.id
        picking.message_subscribe(partner_ids=[responsible_partner_id])
        picking.message_post(
            body=_("A new packed picking has been created and assigned to you."),
            subject=_("New Packed Picking Notification"),
            partner_ids=[responsible_partner_id],
            subtype_xmlid="mail.mt_comment",
        )
        _logger.info(
            f"Notification sent to responsible user ID: {self.responsible_user_id.id}"
        )

    def _get_picking_action(self, picking_id):
        """
        Returns an action dictionary to open the picking form view.

        Args:
            picking_id (int): ID of the created picking.

        Returns:
            dict: An Odoo action dictionary for the picking form view.
        """
        return {
            "type": "ir.actions.act_window",
            "name": _("Picking"),
            "res_model": "stock.picking",
            "res_id": picking_id,
            "view_mode": "form",
            "target": "current",
        }


class TestTaskPackedPickingLineWizard(models.TransientModel):
    """Line wizard for specifying products
    and quantities in packed picking creation."""

    _name = "test.task.packed.picking.line.wizard"
    _description = "Test Task Packed Picking Line Wizard"

    # Fields
    product_id = fields.Many2one(comodel_name="product.product", required=True)
    qty_done = fields.Float(string="Quantity Done", required=True)
    serial = fields.Char()
    wizard_id = fields.Many2one(
        comodel_name="test.task.packed.picking.wizard",
    )

# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Product(models.Model):
    _inherit = "product.product"

    @api.onchange(
        "product_length", "product_height", "product_width", "dimensional_uom_id"
    )
    def onchange_calculate_volume(self):
        self.volume = self.env["product.template"]._calc_volume(
            self.product_length,
            self.product_height,
            self.product_width,
            self.dimensional_uom_id,
        )

    @api.model
    def _get_dimension_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]

    product_length = fields.Float("length")
    product_height = fields.Float("height")
    product_width = fields.Float("width")
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        domain=lambda self: self._get_dimension_uom_domain(),
        help="UoM for length, height, width",
        default=lambda self: self.env.ref("uom.product_uom_meter"),
    )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _calc_volume(self, product_length, product_height, product_width, uom_id):
        volume = 0
        if product_length and product_height and product_width and uom_id:
            length = self.convert_to_volume_uom(product_length, uom_id)
            height = self.convert_to_volume_uom(product_height, uom_id)
            width = self.convert_to_volume_uom(product_width, uom_id)
            volume = length * height * width

        return volume

    @api.onchange(
        "product_length", "product_height", "product_width", "dimensional_uom_id"
    )
    def onchange_calculate_volume(self):
        self.volume = self._calc_volume(
            self.product_length,
            self.product_height,
            self.product_width,
            self.dimensional_uom_id,
        )

    def convert_to_volume_uom(self, measure, dimensional_uom):

        IrParamSudo = self.env['ir.config_parameter'].sudo()
        volume_in_cubic_feet = IrParamSudo.get_param('product.volume_in_cubic_feet')
        if volume_in_cubic_feet == '1':
            to_unit_uom = self.env.ref("uom.product_uom_foot")
        else:
            to_unit_uom = self.env.ref("uom.product_uom_meter")

        return dimensional_uom._compute_quantity(
            qty=measure,
            to_unit=to_unit_uom,
            round=False,
        )

    # Define all the related fields in product.template with 'readonly=False'
    # to be able to modify the values from product.template.
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        related="product_variant_ids.dimensional_uom_id",
        help="UoM for length, height, width",
        readonly=False,
    )

    product_length = fields.Float(
        related="product_variant_ids.product_length", readonly=False
    )
    product_height = fields.Float(
        related="product_variant_ids.product_height", readonly=False
    )
    product_width = fields.Float(
        related="product_variant_ids.product_width", readonly=False
    )

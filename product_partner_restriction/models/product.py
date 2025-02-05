from odoo import fields, models


class Product(models.Model):
    _inherit = "product.product"

    restrict_to_partner_ids = fields.Many2many(
        related="product_tmpl_id.restrict_to_partner_ids", string="Partners"
    )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    restrict_to_partner_ids = fields.Many2many("res.partner", string="Partners")

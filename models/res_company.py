from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    # 7span customization
    show_contract_name = fields.Boolean(default=True, string="Show Contract Name")
    show_vendor_id = fields.Boolean(default=True, string="Show Vendor")
    show_customer_id = fields.Boolean(default=True, string="Show Customer")
    show_start_date = fields.Boolean(default=True, string="Show Start Date")
    show_end_date = fields.Boolean(default=True, string="Show End Date")
    show_currency_id = fields.Boolean(default=True, string="Show Currency")
    show_flag = fields.Boolean(default=True, string="Show Flag")
    show_product_lines = fields.Boolean(default=True, string="Show Product Lines")
    show_create_date = fields.Boolean(default=True, string="Show Created Date")
    show_state = fields.Boolean(default=True, string="Show Status")

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    # 7span customization
    show_contract_name = fields.Boolean(string="Show Contract Name")
    show_vendor_id = fields.Boolean(string="Show Vendor")
    show_customer_id = fields.Boolean(string="Show Customer")
    show_start_date = fields.Boolean(string="Show Start Date")
    show_end_date = fields.Boolean(string="Show End Date")
    show_currency_id = fields.Boolean(string="Show Currency")
    show_flag = fields.Boolean(string="Show Flag")
    show_product_lines = fields.Boolean(string="Show Product Lines")
    show_create_date = fields.Boolean(string="Show Created Date")
    show_state = fields.Boolean(string="Show Status")

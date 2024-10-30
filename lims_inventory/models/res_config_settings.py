from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pay_invoices_online = fields.Boolean(
        string="Pay Invoices Online", config_parameter="account.pay_invoices_online"
    )

    # 7span customization
    show_contract_name = fields.Boolean(
        readonly=False,
        string="Show Contract Name",
        related="company_id.show_contract_name",
    )
    show_vendor_id = fields.Boolean(
        readonly=False, string="Show Vendor", related="company_id.show_vendor_id"
    )
    show_customer_id = fields.Boolean(
        readonly=False, string="Show Customer", related="company_id.show_customer_id"
    )
    show_start_date = fields.Boolean(
        readonly=False, string="Show Start Date", related="company_id.show_start_date"
    )
    show_end_date = fields.Boolean(
        readonly=False, string="Show End Date", related="company_id.show_end_date"
    )
    show_currency_id = fields.Boolean(
        readonly=False, string="Show Currency", related="company_id.show_currency_id"
    )
    show_product_lines = fields.Boolean(
        readonly=False,
        string="Show Product Lines",
        related="company_id.show_product_lines",
    )
    show_create_date = fields.Boolean(
        readonly=False,
        string="Show Created Date",
        related="company_id.show_create_date",
    )
    show_state = fields.Boolean(
        readonly=False, string="Show Status", related="company_id.show_state"
    )

from odoo import models, fields

class LaboratoryHub(models.Model):
    _name = 'lims.laboratory.hub'
    _description = 'Laboratory Hub'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Hub Name', required=True, tracking=True)
    code = fields.Char(string='Hub Code', tracking=True)
    address = fields.Text(string='Address', tracking=True)

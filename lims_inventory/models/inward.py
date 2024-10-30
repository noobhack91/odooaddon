from odoo import models, fields, api, _

class InwardReceipt(models.Model):
  _name = 'lims.inward.receipt'
  _description = 'Inward Receipt'
  _inherit = ['mail.thread', 'mail.activity.mixin']

  name = fields.Char(string='Receipt Number', required=True, copy=False, readonly=True, default='New', tracking=True)
  date = fields.Date(string='Receipt Date', default=fields.Date.today, tracking=True)
  indent_id = fields.Many2one('lims.purchase.indent', string='Related Indent', tracking=True)
  line_ids = fields.One2many('lims.inward.receipt.line', 'receipt_id', string='Receipt Lines')

  @api.model
  def create(self, vals):
      if vals.get('name', 'New') == 'New':
          vals['name'] = self.env['ir.sequence'].next_by_code('lims.inward.receipt') or 'New'
      return super(InwardReceipt, self).create(vals)

class InwardReceiptLine(models.Model):
  _name = 'lims.inward.receipt.line'
  _description = 'Inward Receipt Line'

  receipt_id = fields.Many2one('lims.inward.receipt', string='Receipt')
  product_id = fields.Many2one('lims.inventory.item', string='Item', required=True)
  quantity = fields.Float(string='Quantity', required=True)
  uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
  specifications = fields.Text(string='Specifications')

  @api.onchange('product_id')
  def onchange_product_id(self):
      if self.product_id:
          self.uom_id = self.product_id.uom_id.id
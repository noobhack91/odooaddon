from odoo import models, fields, api, _

class ItemTransaction(models.Model):
  _name = 'lims.item.transaction'
  _description = 'Item Transaction'
  _inherit = ['mail.thread', 'mail.activity.mixin']

  name = fields.Char(string='Transaction Reference', required=True, copy=False, readonly=True, default='New', tracking=True)
  date = fields.Datetime(string='Transaction Date', default=fields.Datetime.now, tracking=True)
  item_id = fields.Many2one('lims.inventory.item', string='Item', required=True, tracking=True)
  quantity = fields.Float(string='Quantity', required=True, tracking=True)
  transaction_type = fields.Selection([
      ('issue', 'Issue'),
      ('return', 'Return'),
  ], string='Transaction Type', required=True, tracking=True)
  user_id = fields.Many2one('res.users', string='Responsible User', default=lambda self: self.env.user, tracking=True)
  test_id = fields.Many2one('lims.test', string='Related Test', tracking=True)

  @api.model
  def create(self, vals):
      if vals.get('name', 'New') == 'New':
          vals['name'] = self.env['ir.sequence'].next_by_code('lims.item.transaction') or 'New'
      return super(ItemTransaction, self).create(vals)

  def action_issue(self):
      self.ensure_one()
      if self.transaction_type == 'issue':
          self.item_id.qty_available -= self.quantity
      elif self.transaction_type == 'return':
          self.item_id.qty_available += self.quantity

class LIMSTest(models.Model):
  _name = 'lims.test'
  _description = 'LIMS Test'
  _inherit = ['mail.thread', 'mail.activity.mixin']

  name = fields.Char(string='Test Name', required=True, tracking=True)
  code = fields.Char(string='Test Code', tracking=True)
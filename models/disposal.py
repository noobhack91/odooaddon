from odoo import models, fields, api, _

class AssetDisposal(models.Model):
  _name = 'lims.asset.disposal'
  _description = 'Asset Disposal'
  _inherit = ['mail.thread', 'mail.activity.mixin']

  name = fields.Char(string='Disposal Reference', required=True, copy=False, readonly=True, default='New', tracking=True)
  asset_id = fields.Many2one('lims.inventory.item', string='Asset', domain=[('is_asset', '=', True)], required=True, tracking=True)
  disposal_date = fields.Date(string='Disposal Date', required=True, tracking=True)
  reason = fields.Text(string='Reason for Disposal', required=True, tracking=True)
  method = fields.Selection([
      ('scrap', 'Scrap'),
      ('sell', 'Sell'),
      ('donate', 'Donate'),
  ], string='Disposal Method', required=True, tracking=True)
  responsible_user_id = fields.Many2one('res.users', string='Responsible User', default=lambda self: self.env.user, tracking=True)
  state = fields.Selection([
      ('draft', 'Draft'),
      ('disposed', 'Disposed'),
  ], string='Status', default='draft', tracking=True)

  @api.model
  def create(self, vals):
      if vals.get('name', 'New') == 'New':
          vals['name'] = self.env['ir.sequence'].next_by_code('lims.asset.disposal') or 'New'
      return super(AssetDisposal, self).create(vals)

  def action_dispose(self):
      self.ensure_one()
      self.asset_id.write({'active': False})
      self.write({'state': 'disposed'})
      return True
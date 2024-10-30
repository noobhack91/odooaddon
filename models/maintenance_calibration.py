from odoo import models, fields, api, _

class MaintenanceRecord(models.Model):
  _name = 'lims.maintenance.record'
  _description = 'Maintenance Record'
  _inherit = ['mail.thread', 'mail.activity.mixin']

  name = fields.Char(string='Maintenance Reference', required=True, copy=False, readonly=True, default='New', tracking=True)
  asset_id = fields.Many2one('lims.inventory.item', string='Asset', domain=[('is_asset', '=', True)], required=True, tracking=True)
  date = fields.Date(string='Maintenance Date', required=True, tracking=True)
  maintenance_type = fields.Selection([
      ('maintenance', 'Maintenance'),
      ('calibration', 'Calibration'),
  ], string='Type', required=True, tracking=True)
  consultant_id = fields.Many2one('lims.maintenance.consultant', string='Consultant', tracking=True)
  issues = fields.Text(string='Issues', tracking=True)
  actions = fields.Text(string='Actions Taken', tracking=True)
  responsible_user_id = fields.Many2one('res.users', string='Responsible User', default=lambda self: self.env.user, tracking=True)
  next_due_date = fields.Date(string='Next Due Date', tracking=True)

  @api.model
  def create(self, vals):
      if vals.get('name', 'New') == 'New':
          vals['name'] = self.env['ir.sequence'].next_by_code('lims.maintenance.record') or 'New'
      return super(MaintenanceRecord, self).create(vals)

  @api.onchange('asset_id', 'maintenance_type', 'date')
  def _onchange_asset_maintenance(self):
      if self.asset_id and self.maintenance_type and self.date:
          if self.asset_id.maintenance_schedule == 'daily':
              self.next_due_date = fields.Date.add(self.date, days=1)
          elif self.asset_id.maintenance_schedule == 'weekly':
              self.next_due_date = fields.Date.add(self.date, weeks=1)
          elif self.asset_id.maintenance_schedule == 'monthly':
              self.next_due_date = fields.Date.add(self.date, months=1)
          elif self.asset_id.maintenance_schedule == 'quarterly':
              self.next_due_date = fields.Date.add(self.date, months=3)
          elif self.asset_id.maintenance_schedule == 'yearly':
              self.next_due_date = fields.Date.add(self.date, years=1)
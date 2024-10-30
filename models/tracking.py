from odoo import models, fields, api

class LaboratoryConsumptionTracking(models.Model):
  _name = 'lims.consumption.tracking'
  _description = 'Laboratory Consumption Tracking'
  _inherit = ['mail.thread', 'mail.activity.mixin']

  date = fields.Date(string='Date', default=fields.Date.today, tracking=True)
  laboratory_id = fields.Many2one('lims.laboratory', string='Laboratory', required=True, tracking=True)
  item_id = fields.Many2one('lims.inventory.item', string='Item', required=True, tracking=True)
  quantity_consumed = fields.Float(string='Quantity Consumed', required=True, tracking=True)
  uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='item_id.uom_id', readonly=True)

  @api.model
  def create(self, vals):
      record = super(LaboratoryConsumptionTracking, self).create(vals)
      record.item_id.qty_available -= record.quantity_consumed
      return record

class Laboratory(models.Model):
  _name = 'lims.laboratory'
  _description = 'Laboratory'
  _inherit = ['mail.thread', 'mail.activity.mixin']

  name = fields.Char(string='Laboratory Name', required=True, tracking=True)
  code = fields.Char(string='Laboratory Code', tracking=True)
  hub_id = fields.Many2one('lims.laboratory.hub', string='Hub', tracking=True)
  address = fields.Text(string='Address', tracking=True)
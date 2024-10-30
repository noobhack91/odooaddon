from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError
from datetime import timedelta
from odoo.exceptions import UserError
from datetime import datetime

class PurchaseIndent(models.Model):
    _name = 'lims.purchase.indent'
    _description = 'Purchase Indent'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Indent Number',
        required=True,
        copy=False,
        readonly=True,
        default='New',
        tracking=True
    )
    date = fields.Date(
        string='Date',
        default=fields.Date.today,
        tracking=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('close', 'Close'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)
    
    line_ids = fields.One2many(
        'lims.purchase.indent.line', 
        'indent_id', 
        string='Indent Lines'
    )

    is_amc = fields.Boolean(string='Is AMC', tracking=True)
    tender_reference = fields.Char(string='Tender Reference', tracking=True)
    hub_id = fields.Many2one(
        'lims.laboratory.hub', 
        string='Hub', 
        tracking=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        tracking=True
    )
    create_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
        tracking=True
    )
    expected_delivery_date = fields.Date(
        string='Expected Delivery Date', 
        tracking=True
    )
   
    @api.constrains('expected_delivery_date')
    def _check_expected_delivery_date(self):
        for record in self:
            if record.expected_delivery_date:
                if record.expected_delivery_date >= fields.Date.today():
                    raise ValidationError("The Expected Delivery Date must be at least one day in the past.")
    
    @api.constrains('line_ids')
    def _check_lines_when_approved(self):
        for record in self:
            if record.state == 'approved':
                # Check if any line is being created or deleted
                if any(line.id for line in record.line_ids):
                    raise ValidationError("Cannot create or delete item lines when the purchase indent is approved.")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('lims.purchase.indent') or 'New'
        return super(PurchaseIndent, self).create(vals)
    
    def write(self, vals):
        for record in self:
            if record.state  in ['approved','rejected']:
                raise ValidationError("You cannot edit an approved Purchase Indent.")
        return super(PurchaseIndent, self).write(vals)
        
    # Optional: Create a method to change state
    def action_submit(self):
        self.state = 'submitted'

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'


class PurchaseIndentLine(models.Model):
    _name = 'lims.purchase.indent.line'
    _description = 'Purchase Indent Line'

    indent_id = fields.Many2one(
        'lims.purchase.indent',
        string='Indent',
        required=True,
        ondelete='cascade'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )
    quantity = fields.Float(string='Quantity', required=True)
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        required=True
    )
    specifications = fields.Text(string='Specifications')
    po_quantity = fields.Float(string="PO Quantity", required=False)


class PurchaseOrder(models.Model):
    _name = 'lims.purchase.order'
    _description = 'Purchase Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Order Number', required=True, copy=False, readonly=True, default='New', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, domain=[('active', '=', True)], tracking=True)

    vendor_id = fields.Many2one('res.partner', string='Vendor', domain="[('is_company', '=', True)]", required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', domain="[('is_company', '=', False)]")

    indent_id = fields.Many2one(
        'lims.purchase.indent',
        string='Indent',
        required=True,
        ondelete='cascade',
        options={'no_create': True, 'no_create_edit': True}
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('close', 'Close'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)
   
    narration = fields.Text(string='Narration', help='Up to 1000 characters', limit=1000)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, tracking=True)
    create_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user, readonly=True, tracking=True)
   
    order_line_ids = fields.One2many('lims.purchase.order.line', 'purchase_order_id', string='Order Lines', options={'no_create': True, 'no_create_edit': True})

    @api.onchange('indent_id')
    def _onchange_indent_id(self):
        if self.indent_id:
            lines = self.indent_id.line_ids 
            self.order_line_ids = [(5, 0, 0)]  
            for line in lines:
                vendor_rate = self.env['lims.vendor.rate.contract.line'].search([
                    ('product_id', '=', line.product_id.id),
                    ('contract_id.vendor_id', '=', self.vendor_id.id),  # Make sure vendor_id is set
                ], limit=1)  # You might want to handle multiple contracts based on your logic
                print('price',vendor_rate.price)
                price = vendor_rate.price if vendor_rate else 0.00
                if line.quantity > 0:  # Example condition

                    self.order_line_ids |= self.env['lims.purchase.order.line'].new({
                        'product_id': line.product_id.id,
                        'price':price,
                        'quantity': line.quantity - line.po_quantity,
                    })

  
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            current_year = fields.Date.today().year
            last_order = self.search([], order='id desc', limit=1)
            
            if last_order:
                last_order_number = last_order.name.split('/')[-1]
                next_order_number = int(last_order_number) + 1
            else:
                next_order_number = 1
            vals['name'] = f"PO/{current_year}/{str(next_order_number).zfill(6)}"
            
        return super(PurchaseOrder, self).create(vals)
    
    def write(self, vals):
        for record in self: 
            if record.state  in ['approved','rejected']:
                raise ValidationError("You cannot edit an approved Purchase Order.")
        return super(PurchaseOrder, self).write(vals)
        
    # Optional: Create a method to change state
    def action_submit(self):
        self.state = 'submitted'

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'


class PurchaseOrderLine(models.Model):
    _name = 'lims.purchase.order.line'
    _description = 'Purchase Order Line'

    purchase_order_id = fields.Many2one('lims.purchase.order', string='Purchase Order')
    product_id = fields.Many2one('product.product', string='Product', readonly=True)  # Read-only field
    quantity = fields.Float(string='Quantity')
    grn_quantity = fields.Float(string="PO Quantity")
    price = fields.Float(string="PO Price")

    # Method to update product_id programmatically
    @api.onchange('purchase_order_id')
    def _onchange_purchase_order_id(self):
        if self.purchase_order_id:
            indent_lines = self.purchase_order_id.indent_id.line_ids 
            self.product_id = False
            for line in indent_lines:
                if line.product_id:  
                    self.product_id = line.product_id.id  
                    self.quantity = line.quantity  

    # Programmatically update product_id when creating a new line
    @api.model
    def create(self, vals):
        if 'purchase_order_id' in vals:
            purchase_order = self.env['lims.purchase.order'].browse(vals['purchase_order_id'])
            for line in purchase_order.indent_id.line_ids:
                if line.product_id:
                    vals.update({'product_id': line.product_id.id}) 
                    vals.update({'quantity': line.quantity})  
        return super(PurchaseOrderLine, self).create(vals)
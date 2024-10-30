from odoo import http
from odoo.http import request
import json

class VendorAPIController(http.Controller):
    @http.route('/api/vendors', type='http', auth='public', methods=['GET'])
    def get_vendors(self, is_company=False, **kw):
        vendors = request.env['res.partner'].sudo().search([
            ('is_company', '=', is_company)
        ])
        vendor_list = [{
            'id': vendor.id,
            'name': vendor.name,
            'email': vendor.email,
            'phone': vendor.phone,
            'country_id': vendor.country_id.name if vendor.country_id else None,
            'city': vendor.city,
            'is_company': vendor.is_company
        } for vendor in vendors]

        #print(vendor_list)
        # Return JSON response
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',  # Change to your frontend domain in production
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return request.make_response(
            json.dumps({'vendors': vendor_list}),
            headers=headers
        )

class ProductAPIController(http.Controller):

    @http.route('/api/products', type='http', auth='public', methods=['GET', 'OPTIONS'])
    def get_products(self, **kw):
        # Handle preflight CORS request
        if request.httprequest.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',  # Change to your frontend domain in production
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            }
            return request.make_response('', headers=headers)

        # Fetch all products
        products = request.env['product.template'].sudo().search([])

        # Create a list of product details
        product_list = [{
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'list_price': product.list_price,
            'categ_id': product.categ_id.name if product.categ_id else None,
            'quantity_available': product.qty_available,  # Ensure the product model has this field
        } for product in products]

        # Set CORS headers and return JSON response
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',  # Change to your frontend domain in production
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }

        return request.make_response(
            json.dumps({'products': product_list}),
            headers=headers
        )

from odoo import http
from odoo.http import request

class ContractManagementController(http.Controller):
    @http.route('/contract_management', type='http', auth='user', website=True)
    def contract_management(self, **kwargs):
        return request.render('lims_inventory.ContractManagementTemplate')
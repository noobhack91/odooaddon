from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.product"

    sale_ok = fields.Boolean(default=False)
    purchase_ok = fields.Boolean(default=False)


class ProductCategory(models.Model):
    _inherit = "product.category"  # Inheriting the existing model

    @api.constrains("name", "parent_id")
    def _check_unique_name(self):
        for record in self:
            if record.parent_id:
                existing_categories = self.search(
                    [
                        ("name", "ilike", record.name),
                        ("parent_id", "=", record.parent_id.id),
                        ("id", "!=", record.id),
                    ]
                )
            else:
                existing_categories = self.search(
                    [
                        ("name", "ilike", record.name),
                        ("parent_id", "=", False),
                        ("id", "!=", record.id),
                    ]
                )
            if existing_categories:
                raise ValidationError(
                    "A category with the name '%s' already exists." % record.name
                )


class InventoryCategory(models.Model):
    _name = "lims.inventory.category"
    _description = "Inventory Category"

    name = fields.Char(string="Name", required=True)
    parent_id = fields.Many2one("lims.inventory.category", string="Parent Category")
    child_ids = fields.One2many(
        "lims.inventory.category", "parent_id", string="Subcategories"
    )

    # Constraint to check for duplicate names

    @api.constrains("name", "parent_id")
    def _check_unique_name(self):
        for record in self:
            if record.parent_id:
                existing_categories = self.search(
                    [
                        ("name", "ilike", record.name),
                        ("parent_id", "=", record.parent_id.id),
                        ("id", "!=", record.id),
                    ]
                )
            else:
                existing_categories = self.search(
                    [
                        ("name", "ilike", record.name),
                        ("parent_id", "=", False),
                        ("id", "!=", record.id),
                    ]
                )

            if existing_categories:
                raise ValidationError(
                    "A category with the name '%s' already exists." % record.name
                )


class InventoryItemType(models.Model):
    _name = "lims.inventory.item_type"
    _description = "Inventory Item Type"

    name = fields.Char(string="Item Type Name", required=True)
    description = fields.Text(string="Description")

    # Add the 'active' boolean field
    active = fields.Boolean(string="Active", default=True)


class InventoryItem(models.Model):
    _name = "lims.inventory.item"
    _description = "Inventory Item"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", required=True, tracking=True)
    category_id = fields.Many2one(
        "lims.inventory.category", string="Category", tracking=True
    )
    subcategory_id = fields.Many2one(
        "lims.inventory.category", string="Subcategory", tracking=True
    )
    item_type = fields.Selection(
        [
            ("consumable", "Consumable"),
            ("reagent", "Reagent"),
            ("instrument", "Instrument"),
            ("equipment", "Equipment"),
            ("accessory", "Accessory/Spare"),
        ],
        string="Item Type",
        required=True,
        tracking=True,
    )
    is_asset = fields.Boolean(string="Is Asset", tracking=True)
    maintenance_schedule = fields.Selection(
        [
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("yearly", "Yearly"),
        ],
        string="Maintenance Schedule",
        tracking=True,
    )
    supplier_ids = fields.Many2many("res.partner", string="Suppliers", tracking=True)
    qty_available = fields.Float(string="Quantity on Hand", default=0.0, tracking=True)
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure", required=True)


class Supplier(models.Model):
    _inherit = "res.partner"

    is_lab_supplier = fields.Boolean(string="Is Lab Supplier")
    supplied_item_ids = fields.Many2many("lims.inventory.item", string="Supplied Items")


class MaintenanceConsultant(models.Model):
    _name = "lims.maintenance.consultant"
    _description = "Maintenance Consultant"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", required=True, tracking=True)
    contact = fields.Char(string="Contact", tracking=True)
    specialization = fields.Char(string="Specialization", tracking=True)
    asset_ids = fields.Many2many(
        "lims.inventory.item", string="Serviced Assets", tracking=True
    )


class LaboratoryHub(models.Model):
    _name = "lims.laboratory.hub"
    _description = "Laboratory Hub"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Hub Name", required=True, tracking=True)
    code = fields.Char(string="Hub Code", tracking=True)
    address = fields.Text(string="Address", tracking=True)


class VendorRateContract(models.Model):

    _name = "lims.vendor.rate.contract"
    _description = "Vendor Rate Contract"

    name = fields.Char(
        string="Contract Name", compute="_compute_contract_name", store=True
    )
    vendor_id = fields.Many2one(
        "res.partner",
        string="Vendor",
        domain="[('is_company', '=', True)]",
        required=True,
    )
    customer_id = fields.Many2one(
        "res.partner", string="Customer", domain="[('is_company', '=', False)]"
    )
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date")
    currency_id = fields.Many2one("res.currency", string="Currency", required=True)
    active = fields.Boolean(string="Active", default=True)
    flag = fields.Boolean(string="Flag")
    product_line_ids = fields.One2many(
        "lims.vendor.rate.contract.line", "contract_id", string="Product Lines"
    )
    create_date = fields.Datetime(string="Created Date", readonly=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )

    # 7span customization
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
        compute="_compute_company_id",
        required=True,
    )

    # 7span customization
    def _compute_company_id(self):
        for record in self:
            record.company_id = self.env.company

    # 7span customization
    show_contract_name = fields.Boolean(
        string="Show Contract Name", related="company_id.show_contract_name"
    )
    show_vendor_id = fields.Boolean(
        string="Show Vendor", related="company_id.show_vendor_id"
    )
    show_customer_id = fields.Boolean(
        string="Show Customer", related="company_id.show_customer_id"
    )
    show_start_date = fields.Boolean(
        string="Show Start Date", related="company_id.show_start_date"
    )
    show_end_date = fields.Boolean(
        string="Show End Date", related="company_id.show_end_date"
    )
    show_currency_id = fields.Boolean(
        string="Show Currency", related="company_id.show_currency_id"
    )
    show_product_lines = fields.Boolean(
        string="Show Product Lines", related="company_id.show_product_lines"
    )
    show_create_date = fields.Boolean(
        string="Show Created Date", related="company_id.show_create_date"
    )
    show_state = fields.Boolean(string="Show Status", related="company_id.show_state")

    @api.depends("vendor_id", "create_date")
    def _compute_contract_name(self):
        for record in self:
            if record.vendor_id and record.create_date:
                create_date_str = fields.Datetime.to_string(record.create_date)
                record.name = f"{record.vendor_id.name} - {create_date_str}"
            else:
                record.name = "New Contract"  # Default if fields are not yet set

    @api.constrains("start_date", "end_date")
    def _check_start_end_dates(self):
        for record in self:
            if record.end_date and record.start_date:
                if record.end_date < record.start_date:
                    raise ValidationError(
                        "The End Date cannot be earlier than the Start Date."
                    )

    @api.constrains("product_line_ids")
    def _check_product_lines(self):
        for record in self:
            if not record.product_line_ids:
                raise ValidationError("At least one product line is required.")

    @api.model
    def add_product_line(self):
        self.ensure_one()
        self.product_line_ids.create(
            {
                "contract_id": self.id,
                "product_id": False,  # Optionally, you can set a default product here
                "price": 0.0,
            }
        )

    def write(self, vals):
        for record in self:
            if record.state in ["approved", "rejected"]:
                raise ValidationError(
                    "You cannot edit an approved Vendor Rate Contract."
                )
        return super(VendorRateContract, self).write(vals)

    # Optional: Create a method to change state
    def action_submit(self):
        self.state = "submitted"

    def action_approve(self):
        self.state = "approved"

    def action_reject(self):
        self.state = "rejected"


class VendorRateContractLine(models.Model):
    _name = "lims.vendor.rate.contract.line"
    _description = "Vendor Rate Contract Line"

    contract_id = fields.Many2one(
        "lims.vendor.rate.contract", string="Contract", required=True
    )
    product_id = fields.Many2one("product.product", string="Product", required=True)
    price = fields.Float(string="Price", required=True)

    _sql_constraints = [
        (
            "unique_contract_product",
            "UNIQUE(contract_id, product_id)",
            "Each product must be unique within the same contract.",
        )
    ]

    @api.constrains("contract_id", "product_id")
    def _check_unique_contract_product(self):
        for record in self:
            existing_lines = self.search(
                [
                    ("contract_id", "=", record.contract_id.id),
                    ("product_id", "=", record.product_id.id),
                    ("id", "!=", record.id),  # Exclude current record from the search
                ]
            )
            if existing_lines:
                raise ValidationError(
                    "Each product must be unique within the same contract."
                )

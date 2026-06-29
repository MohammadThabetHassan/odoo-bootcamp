from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    best_price = fields.Float(compute="_compute_best_price", store=True)
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )
    date_availability = fields.Date()
    sales_person_id = fields.Many2one("res.users", string="Sales Person")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    def action_sell(self):
        if self.state != "offer_accepted":
            raise UserError("You can only mark as sold when an offer has been accepted.")
        self.state = "sold"
        return True

    def action_cancel(self):
        if self.state == "sold":
            raise UserError("You cannot cancel a property that has already been sold.")
        self.state = "cancelled"
        return True

    @api.constrains("expected_price")
    def _check_expected_price_positive(self):
        for record in self:
            if record.expected_price and record.expected_price <= 0:
                raise ValidationError("Expected price must be strictly positive.")

    @api.constrains("selling_price")
    def _check_selling_price_positive(self):
        for record in self:
            if record.selling_price and record.selling_price <= 0:
                raise ValidationError("Selling price must be strictly positive.")

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_min(self):
        for record in self:
            if record.selling_price and record.expected_price:
                if record.selling_price < (record.expected_price * 0.9):
                    raise ValidationError("Selling price must be at least 90% of expected price.")

    _sql_constraints = [
        ("check_expected_price_positive", "CHECK(expected_price > 0)", "Expected price must be strictly positive."),
    ]
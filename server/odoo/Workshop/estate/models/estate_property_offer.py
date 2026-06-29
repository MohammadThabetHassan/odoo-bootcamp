from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
        default="draft",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = fields.Date.to_date(
                    record.create_date + relativedelta(days=record.validity)
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = fields.Date.to_date(record.date_deadline) - fields.Date.to_date(record.create_date)
                record.validity = delta.days

    def action_accept(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda o: o.status == "accepted"):
                raise UserError(_("An offer has already been accepted for this property."))
            record.status = "accepted"
            record.property_id.write({
                "buyer_id": record.partner_id.id,
                "selling_price": record.price,
                "state": "offer_accepted",
            })
        return True

    def action_refuse(self):
        for record in self:
            if record.property_id.state == "offer_accepted":
                raise UserError(_("Accepted offers cannot be refused."))
            record.status = "refused"
        return True

    _sql_constraints = [
        ("check_offer_price_positive", "CHECK(price > 0)", "The offer price must be strictly positive."),
    ]

from odoo import models,fields,api
from datetime import timedelta
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    
    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner",required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", string="deadline" ,inverse="_invers_date_deadline")   
    property_state = fields.Selection(related="property_id.status", string="Property Status", store=True, readonly=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    
    _sql_constraints = [
        ('price', 'CHECK(price >= 0)',
         'angka tidak boleh mines.')
    ]
    
    @api.depends("create_date","validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _invers_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta =record.date_deadline - record.create_date.date()
                record.validity = delta.days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_Accept(self):
        for record in self:
            if record.property_id.status == 'sold':
                raise ValidationError("tidak bisa diterima sudah sold")
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.status = 'offer Accepted'
        return True
    
    def action_Refuse(self):
        for record in self:
            record.status = 'refused'
            
    @api.model
    def create(self,vals):
        existing_offer = self.search([("property_id","=", vals["property_id"])])
        for offer in existing_offer:
            if vals["price"] <= offer.price:
                raise ValidationError("penawaran harus lebih besar")
            property = self.env["estate.property"].browse(vals["property_id"])
            property.status = "offer Received"  
        return super(EstatePropertyOffer, self).create(vals)
    
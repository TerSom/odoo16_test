from odoo import fields,models,api
from odoo import Command

class EstatePropertyAccount(models.Model):
    _inherit = 'estate.property'
    
    def action_sold(self):

        result = super(EstatePropertyAccount, self).action_sold()

        invoice_vals = {
            'partner_id': self.buyer_id.id,
            'move_type' : 'out_invoice',
            'journal_id': self.env['account.journal'].search([('type','=','sale')],limit=1).id,
            'invoice_line_ids': [
                Command.create({
                    'name' : 'Selling Price Commission',
                    'quantity' : 1,
                    'price_unit' : self.selling_price * 0.06
                }),
                Command.create({
                    'name' : 'tambahan biaya administrasi',
                    'quantity' : 1,
                    'price_unit' : 100.00
                })
            ]
        }
        
        self.env['account.move'].create(invoice_vals)
        
        return result
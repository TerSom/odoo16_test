from odoo import fields,models, api
from datetime import date
from odoo.exceptions import UserError, ValidationError


class algoritma_pembelian(models.Model):
    _name = "algoritma.pembelian"
    _description = "algoritma pembelian"
    _order = 'title asc'
    
    title = fields.Char(string="Title", default="New", readonly=True)
    nama = fields.Char(string="Nama")
    tanggal = fields.Date(string="Tanggal")
    status = fields.Selection(string="Status",
         selection=[
            ('draft','Draft'),
            ('to_approve','To Approve'),
            ('approved','Approved'),
            ('done','Done'),
            ('canceled','Canceled')
            ],required=True,default="draft"
    )
    algoritma_pembelian_line_ids = fields.One2many('algoritma.pembelian.line','algoritma_pembelian_id' ,string="algoritma pembelian line ids")
    algoritma_brand_ids = fields.Many2many('algoritma.brand','algoritma_brand_rel' , 'algoritma_pembelian_id','brand_id',string="Brand")
    product_name = fields.Char(string="Product Name", related="algoritma_pembelian_line_ids.name" ,store=True)
    
    @api.model
    def create(self,vals):
        if not vals.get('title'):
            seq = self.env['ir.sequence'].next_by_code('algoritma.pembelian') or 'New'
            vals['title'] = seq
                    
        res = super(algoritma_pembelian,self).create(vals)
        for recrod in res:
            tanggal_pembelian = recrod.tanggal
            tanggal_sekarang = date.today()
            if tanggal_pembelian < tanggal_sekarang:
                raise ValidationError("Tanggal pembelian tidak boleh kurang dari tanggal sekrang")
        return res
    
    def write(self,vals):
        res = super(algoritma_pembelian,self).write(vals)
        if 'tanggal' in vals:
            tanggal_pembelian = self.tanggal
            tanggal_sekarang = date.today()
            if tanggal_pembelian < tanggal_sekarang:
                raise ValidationError("Tanggal pembelian tidak boleh kurang dari tanggal sekrang")
        return res
                
    def to_approve(self):
        for record in self:
            if record.status == 'draft':
                record.status = 'to_approve'
    
    def approved(self):
        for record in self:
            if record.status == 'to_approve':
                record.status = 'approved'

    def done(self):
        for record in self:
            if record.status == 'approved':
                record.status = 'done'
    
    def canceled(self):
        for record in self:
            if record.status == 'draft':
                record.status = 'canceled'
    
    
class algoritma_pembelian_line(models.Model):
    _name = "algoritma.pembelian.line"
    
    
    algoritma_pembelian_id = fields.Many2one('algoritma.pembelian', string="algoritma pembelian id")
    product_id = fields.Many2one('product.product',string="product id")
    quantity = fields.Float(string="Quantity", default= 0.0)
    uom_id = fields.Many2one('uom.uom',string="Uom id")
    name = fields.Char(string="Name")
    total_price = fields.Float(default=0.0, string="Total price", compute=('_compute_total_price'))
    sales_price = fields.Float(string="Sales Price" ,default=0.0)
    standar_price = fields.Float(string="Cost" ,default=0.0)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for record in self:
            if not record.product_id:
                return {}
            else:
                record.name = record.product_id.name
                record.sales_price = record.product_id.list_price
                record.standar_price = record.product_id.standard_price
                record.quantity = record.product_id.qty_available
    
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.sales_price * record.quantity - record.standar_price
            
            
class algoritma_brand(models.Model):
    _name = "algoritma.brand"
    
    
    name = fields.Char(string="Name")
    color = fields.Integer()
    
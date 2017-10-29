from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_project_name = fields.Char(string='Project Name')
    x_location_id = fields.Many2one('hr.location', string='Project Location')
    x_start_date = fields.Date(string='Start Date')
    x_end_date = fields.Date(string='End Date')
    x_status = fields.Selection([('active', 'Active'),
                                 ('finish', 'Finished'),
                                 ('block', 'Blocked'),
                                 ('inactive', 'Inactive')], string='Status')
    x_project_details = fields.Char(string='Details')
    x_total_employees = fields.Integer(string='Hired Employees', compute='compute_active_employees')
    x_work_ids = fields.One2many('hr.work.history', 'sale_order_id')

    @api.depends('x_work_ids.status')
    def compute_active_employees(self):
        for record in self:
            record.x_total_employees = len(record.x_work_ids)
            # sum(1 for active_id in record.x_work_ids if active_id.status == 'active')

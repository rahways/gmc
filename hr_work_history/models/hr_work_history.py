from odoo import models, fields, api, _


class HrWorkHist(models.Model):

    _name = 'hr.work.history'

    name = fields.Char(string='Work History Reference', help='This reference will be used across different models')
    civil_number = fields.Char(string='Civil Number', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee Name')
    employee_name = fields.Char(related='employee_id.name', string='Employee Name', readonly=True)
    onsite_designation_id = fields.Many2one('hr.work.type', string='Designation', required=True)
    contract_id = fields.Many2one('hr.contract', string='Contract', required=True, default=False)
    location_id = fields.Many2one('hr.location', string='Location', required=True)
    hire_date = fields.Date(string='Hiring Date')
    dehire_date = fields.Date(string='Dehire Date')
    status = fields.Selection([('active', 'Active'), ('deactive', 'Deactive')], required=True)
    work_lines_ids = fields.One2many('hr.work.history.lines', 'work_history_id')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    company_name = fields.Char(related='sale_order_id.partner_id.name', string='Company')
    total_hours = fields.Float(string='Total Hours', compute='compute_total_working_hours', store=True)

    @api.model
    def create(self, vals):
        if vals:
            vals.update({
                'name': self.env['ir.sequence'].get('hr.work.hist.seq')
            })
        return super(HrWorkHist, self).create(vals)

    @api.depends('work_lines_ids.hours')
    def compute_total_working_hours(self):
        for rec in self:
            for workline in rec.work_lines_ids:
                rec.total_hours += workline.hours

    @api.onchange('civil_number')
    def onchange_employeeid(self):
        res = {}
        print ('current civil number->', self.civil_number)
        if not self.civil_number:
            res['domain'] = {
                'contract_id': ['employee_id', '=', False],
                'employee_id': ['identification_id', '=', False],
            }
            res['value'] = {
                'contract_id': False,
                'employee_id': False
            }
            return res
        self.employee_id = self.env['hr.employee'].search([('identification_id', '=', self.civil_number)])
        if not self.employee_id:
            return {
                'warning':
                    {
                        'title': _('Warning!'),
                        'message': _('No employee found'),
                    },
                'value':
                    {
                        'civil_number': False,
                    }
            }
        self.contract_id = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])[0]
        res['domain'] = {
            'contract_id': [('employee_id', '=', self.employee_id.id)],
            'employee_id': [('identification_id', '=', self.civil_number)],
        }
        return res

    @api.onchange('contract_id')
    def onchange_contractid(self):
        res = {}
        if not self.contract_id:
            res['domain'] = {
                'onsite_designation_id': [('contract_id', '=', False)]
            }
            return res
        res['domain'] = {
            'onsite_designation_id': [('contract_id', '=', self.contract_id.id)]
        }
        return res


class HrWorkHistLines(models.Model):

    _name = 'hr.work.history.lines'

    name = fields.Char(string='Work Period')
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    hours = fields.Float(string='Timesheet Hours', required=True)
    work_history_id = fields.Many2one('hr.work.history')


class HrWorkType(models.Model):
    _name = 'hr.work.type'

    name = fields.Char(string='Work Type', related='product_id.name', store=True)
    product_id = fields.Many2one('product.product', string='Job Name', domain=[('type', '=', 'service')])
    rate = fields.Float(string='Per Hour Rate')
    contract_id = fields.Many2one('hr.contract')


class HrWorkDetails(models.Model):
    _inherit = 'hr.contract'

    work_type_ids = fields.One2many('hr.work.type', 'contract_id')


class HrLocation(models.Model):
    _name = 'hr.location'

    name = fields.Char(string='Location Name')
    code = fields.Char(string='Location Code')
    partner_id = fields.Many2one('res.partner', string='Customer')

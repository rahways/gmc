from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HrAgreement(models.TransientModel):
    _name = 'hr.agreement'

    name = fields.Char(string='Reference')
    date = fields.Date(string='Date')
    civil_no = fields.Char(string='Civil Number')
    employee_id = fields.Many2one('hr.employee')
    employee_name = fields.Char(string='Employee Name', related='employee_id.name', store=True)
    country_id = fields.Many2one(string='Nationality', related='employee_id.country_id', store=True)
    passport = fields.Char(string='Passport', related='employee_id.passport_id', store=True)
    phone = fields.Char(string='Telephone')
    employee_arabic = fields.Char(string='Name(Arabic)')
    nationality_arabic = fields.Char(string='Nationality(Arabic)')
    passport_arabic = fields.Char(string='Passport(Arabic)')

    def print_agreement(self):
        print('Print Agreement ', self.env.context.get('agreement_type'))
        self.ensure_one()
        [data] = self.read()
        print (data)
        if not data.get('employee_id'):
            raise UserError(_('You have to select an Employee. And try again.'))
        employee = self.env['hr.employee'].browse(data['employee_id'])
        datas = {
            'ids': [],
            'model': 'hr.employee',
            'form': data
        }
        return self.env.ref('hr_agreement.agreement_coemployee').report_action(employee, data=datas)

    @api.onchange('civil_no')
    def onchange_civil_nbr(self):
        res = {}
        if not self.civil_no:
            res['domain'] = {
                'employee_id': ['identification_id', '=', False]
            }
            return
        employee = self.env['hr.employee'].search([('identification_id', '=', self.civil_no)])
        if len(employee) > 1:
            return {
                'warning':
                    {
                        'title': _('Warning!'),
                        'message': _('Duplicate Civil Number found'),
                    },
                'value':
                    {
                        'civil_no': False,
                    }
            }
        self.employee_id = employee.id
        if not self.employee_id:
            return {
                'warning':
                    {
                        'title': _('Warning!'),
                        'message': _('No employee found'),
                    },
                'value':
                    {
                        'civil_no': False,
                    }
            }
        return res



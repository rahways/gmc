# -*- coding:utf-8 -*-
from odoo import models, fields, api, _, tools
import odoo.addons.decimal_precision as dp


class HrEmployeeAdvanceManagement(models.Model):
    _name = 'hr.advance'

    name = fields.Char(string='Reference', help='This reference will be used across different models')
    advance_amount = fields.Float(string='Advance Amount', digits=dp.get_precision('Payroll Rate'), required=True,
                                  help='Amount given as an Advance to the employee')
    advance_date = fields.Date(string='Advance Date', required=True, help='Date when the advance is given')
    advance_type_id = fields.Many2one('hr.advance.type', required=True, string='Advance Type')
    advance_description = fields.Char(string='Advance Description', required=True,
                                      help='Reason why the advance is given')
    deduction_method = fields.Selection([('recur', 'Recurring'), ('total', 'Total')], required=True)
    recur_deduction_method = fields.Selection([('amount', 'Amount'), ('percent', 'Percentage')])
    recur_deduction_amount = fields.Float(string='Deduction Amount', digits=dp.get_precision('Payroll Rate'))
    recur_deduction_percent = fields.Float(string='Deduction Percentage', digits=dp.get_precision('Payroll'))
    remaining_amount = fields.Float(string='Remaining Amount', digits=dp.get_precision('Payroll Rate'),
                                    compute='compute_remaining_amount', readonly=True)
    deduction_line_ids = fields.One2many('hr.advance.deduction.line', 'advance_id')
    contract_id = fields.Many2one('hr.contract', string='Employee Contract',
                                  default=lambda self: self.env['hr.contract'])
    employee_civil_no = fields.Char(string='Civil No.', required=True)
    employee_id = fields.Many2one('hr.employee', default=lambda self: self.env['hr.employee'])

    def compute_remaining_amount(self):
        self.remaining_amount = 0.0

    @api.onchange('employee_civil_no')
    def onchange_civil_number(self):
        res = {}
        if not self.employee_civil_no:
            res['domain'] = {
                'contract_id': ['employee_id', '=', False],
                'employee_id': ['identification_id', '=', False]
            }
            return
        self.employee_id = self.env['hr.employee'].search([('identification_id', '=', self.employee_civil_no)])
        if not self.employee_id:
            return {
                'warning':
                    {
                        'title': _('Warning!'),
                        'message': _('No employee found'),
                    },
                'value':
                    {
                        'employee_civil_no': False,
                    }
            }
        self.contract_id = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])[0]
        res['domain'] = {
            'contract_id': [('employee_id', '=', self.employee_id.id)],
            'employee_id': [('identification_id', '=', self.employee_civil_no)]
        }
        return res

    @api.onchange('recur_deduction_percent')
    def compute_recur_deduction_amount(self):
        for record in self:
            record.recur_deduction_amount = record.advance_amount * (record.recur_deduction_percent / 100)

    @api.model
    def sum_deductions(self):
        total_deduc = 0.0
        for deduction in self.deduction_line_ids:
            total_deduc += deduction.deducted_amount
        return total_deduc

    @api.model
    def create(self, vals):
        if vals:
            vals.update({
                'name': self.env['ir.sequence'].get('hr.advance.seq')
            })
        return super(HrEmployeeAdvanceManagement, self).create(vals)

    @api.model
    def create_salary_rule(self):
        print('function triggered')

        rule_id = self.env['hr.salary.rule'].search([('code', '=', 'ADVANCE')])
        if rule_id:
            print('but returned')
            return
        rule_id = self.env['hr.salary.rule'].create(
            {
                'name': 'Employee Advance',
                'code': 'ADVANCE',
                'sequence': 190,
                'category_id': self.env['hr.salary.rule.category'].search([('code', '=', 'DED')]).id,
                'active': True,
                'appears_on_payslip': True,
                'condition_select': 'none',
                'amount_select': 'code',
                'amount_python_compute': 'result = inputs.ADV.amount',
                'quantity': '1.0',
                'amount_fix': 100,
            }
        )
        input_id = self.env['hr.rule.input'].create(
            {
                'name': 'Advance Input',
                'code': 'ADV',
                'input_id': rule_id.id
            }
        )


class HrAdvanceDeductionLine(models.Model):
    _name = 'hr.advance.deduction.line'

    name = fields.Char(string='Deduction Reference')
    advance_id = fields.Many2one('hr.advance', string='Advance Reference')
    payslip_id = fields.Many2one('hr.payslip', string='Payslip', ondelete='cascade')
    deducted_amount = fields.Float(string='Deducted Amount', digits=dp.get_precision('Payroll'))
    # input_line_id = fields.Many2one('hr.payslip.input', string='Input Line')
    contract_id = fields.Many2one('hr.contract', string='Contract')


class HrEmployeeAdvanceDetails(models.Model):
    _inherit = 'hr.contract'
    # print 'hello'
    advance_ids = fields.One2many('hr.advance', 'contract_id')


class HrEmployeeAdvanceType(models.Model):
    _name = 'hr.advance.type'

    name = fields.Char(string='Advance Type', required=True)
    code = fields.Char(string='Code', help='This code will be used to create Salary Rule based on inputs '
                                           'and the same will be used in Other Inputs in Payslips', required=True)


class HrAdvanceReport(models.Model):
    _name = 'hr.advance.report'
    _auto = False
    _order = 'deduction_date desc'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    deduction_id = fields.Many2one('hr.advance.deduction.line', string='Deduction')
    induction_amount = fields.Float('Ind Amount')
    deduction_amount = fields.Float('Ded Amount')
    induction_date = fields.Date('Advance Date')
    deduction_date = fields.Date('Deduction Date')

    @api.model_cr
    def init(self):
        """ Report on Employee Advance and the deductions """
        tools.drop_view_if_exists(self._cr, 'hr_advance_report')
        self._cr.execute(
            """ CREATE OR REPLACE VIEW hr_advance_report AS (
            SELECT
                advance.id AS id,
                advance.employee_id AS employee_id,
                deduction.id AS deduction_id,
                advance.advance_amount AS induction_amount,
                advance.advance_date AS induction_date,
                deduction.deducted_amount AS deduction_amount
            FROM hr_advance AS advance
            LEFT JOIN hr_advance_deduction_line AS deduction ON deduction.advance_id = advance.id
            GROUP BY 
                advance.id,
                advance.employee_id,
                deduction.id,
                advance.advance_amount,
                advance.advance_date,
                deduction.deducted_amount
            )"""
        )

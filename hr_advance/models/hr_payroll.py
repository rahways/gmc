from odoo import models, fields, api, _
# import odoo.addons.decimal_precision as dp


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    deduct_line_ids = fields.One2many('hr.advance.deduction.line', 'payslip_id', string='Deducted Lines')

    @api.model
    def get_inputs(self, contract_ids, date_from, date_to):
        records = super(HrPayslip, self).get_inputs(contract_ids, date_from, date_to)
        deductions = []
        print records
        contracts = self.env['hr.contract'].browse(contract_ids)
        total_advance = 0.0
        for contract in contracts:
            for advance in contract.advance_ids:
                # First calculate the remaining amount of the advance
                remaining_amount = advance.advance_amount - advance.sum_deductions()
                # Perform deduction if the remaining amount is available
                if remaining_amount > 0.0:
                    # If deduction method is 'total', deduct whole amount
                    if advance.deduction_method == 'total':
                        deduction_amount = remaining_amount
                        print 'deduction amount calculation method goes here...'
                    # If deduction method is based on formula, then calculate the deduction amount
                    else:
                        # If the deduction is based on fixed value or percentage
                        deduction_amount = advance.recur_deduction_amount \
                            if remaining_amount > advance.recur_deduction_amount \
                            else remaining_amount

                    deduction_line = {
                        'name': 'Deduction of advance',
                        'advance_id': advance.id,
                        # 'payslip_id': False,
                        'deducted_amount': deduction_amount,
                        # 'input_line_id': adv_input,
                        'contract_id': contract.id,
                    }
                    deductions += [deduction_line]
                    total_advance += deduction_amount

        """
        for rec in self:
            rec.write({'deduct_line_ids': deductions})
        """

        deduction_lines = self.deduct_line_ids.browse([])
        for deduction in deductions:
            deduction_lines += deduction_lines.new(deduction)
        self.deduct_line_ids = deduction_lines

        for record in records:
            if record['code'] == 'ADV':
                record['amount'] = total_advance
        print total_advance
        return records

    @api.model
    def create(self, values):
        print values
        result = super(HrPayslip, self).create(values)
        """
        deduction_line = {
            'employee_adv_id': self.employee_id.id,
            'payslip_id': self.id,
            'deducted_amount': total_advance,
            # 'input_line_id': adv_input,
            'contract_id': contract.id,
        }
        self.write({
            'deduct_line_ids': [(0, 0, deduction_line)]
        })
        """
        return result

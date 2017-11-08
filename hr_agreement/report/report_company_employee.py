# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models
from odoo.exceptions import UserError


class ReportCompanyEmployee(models.AbstractModel):
    _name = 'report.hr_agreement.report_company_employee'

    @api.model
    def get_report_values(self, docids, data=None):
        print('get_report_values() entered')
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        agreement_report = self.env['ir.actions.report']._get_report_from_name('hr_agreement.report_company_employee')
        records = data['form']
        print('data >>>>', data)
        print('doc_ids >>>>', self.ids)
        print('doc_model >>>>', agreement_report.model)
        print('docs >>>>', records)
        return {
            'doc_ids': self.ids,
            'doc_model': agreement_report.model,
            'docs': records,
        }

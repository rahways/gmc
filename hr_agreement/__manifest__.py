# -*- coding: utf-8 -*-

{
    'name': 'Employee Agreement Forms',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
    Different types of agreement forms for the employees
    """,
    'website': 'https://www.salemgroups.com',
    'depends': ['hr_contract', 'hr_payroll', 'hr'],
    'data': [
        'views/hr_agreement_view.xml',
        'views/report_company_employee.xml',
        'views/report_labour_hiring.xml',
        'report/hr_agreement_report.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}

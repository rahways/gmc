# -*- coding: utf-8 -*-

{
    'name': 'Employee Advance Management',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
    All advances taken by all employees can be tracked and analyzed.
    """,
    'website': 'https://www.salemgroups.com',
    'depends': ['hr_contract', 'hr_payroll'],
    'data': [
        'views/hr_advance_view.xml',
        'views/hr_advance_sequence.xml',
        'data/hr_advance_rule.xml',
        'reports/hr_advance_report.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}

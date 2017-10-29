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
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}

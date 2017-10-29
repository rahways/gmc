# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Employee Work History Management',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
        Work history of every employee.
        """,
    'website': 'https://www.salemgroups.com',
    'depends': ['hr_contract', 'hr_payroll', 'account', 'product', 'hr', 'sale'],
    'data': [
        'views/hr_work_history_view.xml',
        'views/sale_order_view.xml',
        'views/hr_work_history_sequence.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}

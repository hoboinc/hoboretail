# -*- coding: utf-8 -*-
{
    'name': "usa_hoboretail",
    'summary': """
       Personalización HOBORETAIL""",
    'description': """
        -
    """,
    'author': "Ing.Jhonny Mack Merino Samillán",
    'website': "www.hoboretail.com ",
    'category': 'Sale',
    'version': '16.0.2.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/mail_template_invoice.xml',
        'views/account_journal_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/product_views.xml',
        'wizard/invoice_partner_massive_wizard.xml',
        'reports/account_invoice_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

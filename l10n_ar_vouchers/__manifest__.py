# -*- coding: utf-8 -*-
{
    'name': 'Localización Argentina Comprobantes para Factura Electrónica',
    'version': '11.0.1.0.5',

    'description': """
    **Comprobantes para Factura Electrónica**

    ¡Felicidades!. Este es el módulo para Generar Comprobantes PDF de
    Factura Electrónica para la implementación de la **Localización Argentina**

    **Escríbenos** a info@mastercore.net
    """,
    'author': 'MASTERCORE',
    'website': 'www.mastercore.net',
    'license': 'AGPL-3',
    'category': 'Localization / Argentina',
    'depends': [
        'account',
        'sale',
        'l10n_ar_base',
        'l10n_ar_account',
        'l10n_ar_einvoice',
    ],
    'data': [
        'template/report_invoice_ar.xml',
        'template/report_layout_ar.xml',
        'template/report_saleorder_ar.xml',
        'data/external_layout_report.xml',
    ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

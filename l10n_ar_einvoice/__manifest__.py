# -*- coding: utf-8 -*-
{
    'name': 'Localización Argentina Factura Electrónica (AFIP)',
    'version': '11.0.1.0.3',

    'description': """
    **Localización ARGENTINA Factura Electrónica (AFIP)**

    ¡Felicidades!. Este es el módulo para Habilitar la Facturación Electrónica
    AFIP para la implementación de la **Localización Argentina** que agrega
    Funcionalidades necesarias para la emisión de comprobantes electrónicos del
    Web Service de Factura Electrónica V1 ("wsfev1") - R.G. N° 2.485,
    para quienes emitan comprobantes "A", "B" y "C" sin detalle de ítem, CAE.

    **Escríbenos** a info@mastercore.net
    """,

    'author': 'MASTERCORE',
    'website': 'www.mastercore.net',
    'license': 'AGPL-3',
    'category': 'Localization / Argentina',

    'depends': [
        'l10n_ar_base',
        'l10n_ar_account',
        'account_cancel',
    ],
    'external_dependencies': {
        'python': ['suds', ]
    },
    'data': [
        'wizard/upload_certificate_views.xml',
        'views/afipws_menuitem.xml',
        'views/afipws_certificate_views.xml',
        'views/afipws_certificate_alias_views.xml',
        'views/afipws_connection_views.xml',
        'views/res_company_views.xml',
        # Comentado en el origen 'wizard/config_view.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        # Componentes de FE
        'wizard/afip_ws_consult_wizard_views.xml',
        'wizard/afip_ws_currency_rate_wizard_views.xml',
        'views/invoice_views.xml',
        'views/invoice_views_cancel.xml',
        'views/account_journal_document_type_views.xml',
        'views/wsfe_error_views.xml',
        'views/account_journal_views.xml',
        'views/product_uom_views.xml',
        'views/res_currency_views.xml',
        'views/menuitem.xml',
        'res_config_views.xml',
        'views/res_company_view.xml',
        'data/afip.wsfe_error.csv',
    ],

    'auto_install': False,
    'application': False,
    'installable': True,
}

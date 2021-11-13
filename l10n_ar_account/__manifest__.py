# -*- coding: utf-8 -*-
{
    'name': 'Localización Argentina Contabilidad',
    'version': '11.0.1.0.8',

    'description': """
    **Localización ARGENTINA Contabilidad**

    ¡Felicidades!. Este es el módulo de Contabilidad para la implementación
    Contable de la **Localización Argentina** que agrega características y
    datos necesarios para un correcto ejercicio fiscal y contable de su empresa

    **¿CÓMO FUNCIONA?**

    Este módulo extiende algunos modelos relacionados a la Aplicación de
    Contabilidad Odoo y crea otros para la integración de la reglamentación
    AFIP en los procesos contables. Adicionalmente se registran datos de
    localización relacionados a estos modelos:

    - 1 Contabilidad y AFIP
        - 1.1 Código de Jurisdicción
        - 1.2 Código de Actividad AFIP
        - 2.3 Categoría IVA Formulario 2002
        - 1.4 Tipo de Documento / Comprobantes / Notas de Débito / Crédito
        - 1.5 Letra de Documento
        - 1.6 Tipo de Responsabilidad AFIP
        - 1.7 Impuestos
        - 1.8 Número de factura
        - 1.9 Ingresos Brutos
        - 1.10 Fecha de Inicio de Actividad
        - 1.11 Validador de Número de Factura
    - 2 Registro de Datos de Localización
        - 2.1 Registro de Etiquetas de Cuentas
        - 2.2 Registro de Letras de Documentos
        - 2.3 Registro de Grupo de Impuestos
        - 2.4 Registro de Tipo de Responsabilidad
        - 2.5 Registro de Códigos AFIP de País
        - 2.6 Registro de Códigos AFIP de Moneda

    **Escríbenos** a info@mastercore.net
    """,

    'author': 'MASTERCORE',
    'website': 'www.mastercore.net',
    'license': 'AGPL-3',
    'category': 'Localization / Argentina',

    'depends': [
        'account',
        'account_document',
        'l10n_ar_base',
        'account_fix',
    ],

    'external_dependencies': {
        'python': ['py3afipws'],
    },

    'data': [
        'wizard/res_partner_update_from_padron_wizard_view.xml',
        'data/menuitem.xml',
        'data/product_data.xml',
        'data/base_validator_data.xml',
        'data/afip_responsability_type.xml',
        'data/account_document_letter.xml',
        'data/account.document.type.csv',
        'data/afip_incoterm.xml',
        'data/res_country_afip_code.xml',
        'data/res_country_cuit.xml',
        'data/product_uom.xml',
        'data/res_currency.xml',
        'data/res_partner.xml',
        'data/account_tax_group.xml',
        'data/res_country_group_data.xml',
        'data/res_company_data.xml',
        'data/afip_vat_f2002_category_data.xml',
        'data/account_account_tag.xml',
        ## TODO analizar y migrar
        ##'data/account_financial_report_data.xml',
        ## 'data/account_payment_term.xml',
        'report/account_ar_vat_line_view.xml',
        'view/account_move_line_view.xml',
        'view/account_move_view.xml',
        'view/res_partner_view.xml',
        'view/res_company_view.xml',
        'view/afip_menuitem.xml',
        'view/afip_incoterm_view.xml',
        'view/account_account_view.xml',
        'view/res_country_view.xml',
        'view/res_currency_view.xml',
        'view/account_fiscal_position_view.xml',
        'view/product_uom_view.xml',
        'view/account_journal_view.xml',
        'view/account_invoice_view.xml',
        'view/afip_responsability_type_view.xml',
        'view/account_document_letter_view.xml',
        'view/account_document_type_view.xml',
        'view/product_template_view.xml',
        'view/afip_activity_view.xml',
        'view/afip_concept_view.xml',
        'view/afip_tax_view.xml',
        'report/invoice_analysis.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
    ],

    'auto_install': False,
    'application': False,
    'installable': True,
}

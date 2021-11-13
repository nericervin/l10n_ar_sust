# -*- coding: utf-8 -*-
{
    'name': 'Localización Argentina Base',
    'version': '11.0.1.0.6',
    'description': """
    **Localización ARGENTINA Base**

    ¡Felicidades!. Este es el módulo Base para la implementación de la
    **Localización Argentina** que agrega características y datos necesarios
    para un correcto ejercicio fiscal de su empresa.

    **¿CÓMO FUNCIONA?**

    Este módulo extiende algunos modelos base de Odoo relacionados a Datos de
    la Compañia/Configuración, Clientes y Proveedores; Datos de las Provincias;
    Datos de Cuenta Bancaria y Moneda. Adicionalmente se registran datos de
    localización relacionados a estos modelos:

    - 1 Datos de Compañia / Clientes / Proveedores
        - 1.1 Tipo de Identificación
        - 1.2 Número de Identificación
        - 1.3 Código AFIP de tipo de Identificación
        - 1.4 Clave Única de Identificación Tributaria (C.U.I.T) AFIP
    - 2 Configuración de Compañia
        - 2.1 Permitir múltiples números de Identificación en Clientes y
        Proveedores
        - 2.2 Restringir números de ID para que sean Únicos
    - 3 Datos de Provincias
        - 3.1 Código AFIP de Provincia
    - 4 Datos de Cuenta Bancaria
        - 4.1 Clave Bancaria Uniforme (C.B.U.)
    - 5 Registro de Datos de Localización
        - 5.1 Registro de Bancos que operan en Argentina
        - 5.2 Registro de Provincias Argentinas con sus respectivos
        códigos AFIP
        - 5.3 Registro de Tipos de Identificación AFIP
        - 5.4 Registro de Títulos de Identificacón comunes

    **Escríbenos** a info@mastercore.net
    """,

    'author': 'MASTERCORE',
    'website': 'www.mastercore.net',
    'license': 'AGPL-3',
    'category': 'Localization / Argentina',

    'depends': [
        'account_document',
        'base',
        'base_setup',
        'partner_identification',
        'sale'
    ],

    'data': [
        'data/res_currency_data.xml',
        # 'data/res_company_data.xml',
        'data/res_country_state_data.xml',
        'data/res_bank_data.xml',
        'data/res_partner_title_data.xml',
        'data/res_partner_id_category_data.xml',
        'views/res_partner_bank_views.xml',
        'views/res_partner_views.xml',
        'views/res_company_views.xml',
        'views/res_partner_id_category_views.xml',
        'views/res_partner_id_number_views.xml',
        'views/sale_config_views.xml',
        'security/security.xml',
    ],

    'auto_install': False,
    'application': False,
    'installable': True,
}

----------------------------------------------

Odoo Argentinian's Localization
=================

----------------------------------------------

### Para testing:
- Crear la bd de testing seleccionando sin seleccionar COUNTRY

### Instalar los módulos en este orden:
- partner_identification
- l10n_ar_base
- account_document
- base_validator
- account_fix
- account_cancel
- currency_rate_update
- l10n_ar_account
- account_check
- l10n_ar_einvoice
- sale_management (opt)
- point_of_sale
- l10n_ar
- read_only_bypass


### Notas de detalles:

- Revisar si se pueden quitar botones de desviación de flujo de carga de
certificado de conexion AFIP
- Corregir saltos de linea en la carga de las claves de certificado de conexión
AFIP
- Issues con los cachés generados de las consultas AFIP
- Revisar si se pueden quitar botones de desviación de flujo de actualizacion
de datos desde AFIP
- Corregir parche del la clase Struct(dict) de py3simplesoap/helpers.py
- Revisar la vista de configuración de l10n_ar_account 'res_config_view.xml',
tenemos problemas con los métodos llamados ahí
- CUIT de My Company cuando lo agregas por primera vez y guardas, no se registra
- Crear validación de tipo de responsabilidad AFIP para creación de Partner.

#### Dependencias externas w/pip3

- python3-openssl | pyOpenSSL
- python3-suds

#### Dependencias externas wip/dev
- py3afipws
- py3simplesoap


----------------------------------------------

TESTING
=================

----------------------------------------------

### Configurar My Company
- Definir Nombre,
- Localización Argentina,
- Tipo de Responsabilidad,
- AFIP authorization verification
- CUIT 30111111118

### Configurar Certificado AFIP
- Type	Homologation
- Service Type
- Private Key
- Confirm
- Create Certificate Request
- Request Certificate
- Certificate
- Confirm
- Save

### Parametro de Homologación
- System Parameters
    "key" afip.ws.env.type
    "value" homologation

### Test AFIP Consulta Padron A4
- Contacts
- Create Individual
- CUIT 20002400783
- Tipo de Responsabilidad / Consumidor Final

### Test Facturación Cliente
- Facturación / Configuración / Contabilidad / Diarios


----------------------------------------------

Docker
=================

----------------------------------------------

## Descargar repositorios:

### Localización Argentina
    git clone https://git.sinapsys.global/farraez/l10n_argentina.git -b wip/account_migration l10n_argentina_v11
### PyAfipWS
    git clone https://github.com/odoo-mastercore/py3afipws.git -b develop l10n_argentina_v11/py3afipws
### PySimpleSOAP
    git clone https://github.com/odoo-mastercore/py3simplesoap.git -b develop l10n_argentina_v11/py3simplesoap
### Descargar imagen de postgresql en docker:
    docker pull postgres:9.4
### Descargar imagen de odoo en docker:
    docker pull odoo:11.0
### Correr contenedor que funcionará como nuestro data storage:
    docker container run -d -e POSTGRES_USER=odoo11 -e POSTGRES_PASSWORD=odoo11 --name db11 postgres
#### Correr contenedor de odoo y ligarlo a los archivos de configuración, carpeta de addons y al contenedor de base de datos:
    docker run -v /home/user/odoo-11.0/:/etc/odoo -v /home/user/l10n_argentina_v11/:/mnt/extra-addons -d -p 80:8069 --name odoo11 --link db11:db -t odoo

Instalación de dependencias en el contenedor de odoo:
--------------------
### Actualizar headers de repositorios de software del contenedor de odoo
    docker container exec -u 0 -it odoo11 apt update
### Instalar Python y PIP
	docker container exec -u 0 -it odoo11 apt install python python-pip -y
### Instalar erppeek
    docker container exec -u 0 -it odoo11 pip install erppeek
### OpenSSL
    docker container exec -u 0 -it odoo11 apt install python3-openssl -y
    docker container exec -u 0 -it odoo11 pip3 install pyOpenSSL==17.5.0
### Crypto
    docker container exec -u 0 -it odoo11 pip3 install crypto
    docker container exec -u 0 -it odoo11 pip3 install asn1crypto==0.24.0
### Cryptography
    docker container exec -u 0 -it odoo11 pip3 install cryptography
### HttpLib2
    docker container exec -u 0 -it odoo11 pip3 install httplib2
Configurar PyAfipWS y PySimpleSOAP en el contenedor de odoo:
--------------------
    docker container exec -u 0 -it odoo11 ln -s /mnt/extra-addons/py3simplesoap/py3simplesoap /usr/lib/python3.5/py3simplesoap
    docker container exec -u 0 -it odoo11 ln -s /mnt/extra-addons/py3afipws /usr/lib/python3.5/py3afipws

Instalar Addons
--------------------
    docker container exec -u 0 -it odoo11 python /mnt/extra-addons/install_addons.py

Notas:
=================

- El archivo de configuración debe estar ubicado dentro de la carpeta que especifiquemos en este caso debe estar dentro de la carpeta «/home/user/odoo-11.0/», y el nombre del archivo	debe ser «odoo.conf»
- La carpeta de addons debe ser la que apunte donde están los repositorios en nuestro caso es en «/home/user/l10n_argentina_v11/»


Reiniciar contenedores:
--------------------
    docker container restart db11 odoo11
Dejar log abierto:
--------------------
    docker container logs -f --tail 20 odoo11

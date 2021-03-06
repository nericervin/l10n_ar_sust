# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
import logging
from odoo.exceptions import UserError
import odoo.tools as tools
import os
import hashlib
import time
import sys
import traceback

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):

    _inherit = "res.company"

    alias_ids = fields.One2many(
        'afipws.certificate_alias',
        'company_id',
        'Aliases',
    )
    connection_ids = fields.One2many(
        'afipws.connection',
        'company_id',
        'Connections',
    )
    ##Campo agregado de l10n_ar_afipws_fe
    afip_auth_verify_type = fields.Selection([
        ('not_available', 'Not Available'),
        ('available', 'Available'),
        ('required', 'Required'),
    ],
        required=True,
        default='not_available',
        string='AFIP authorization verification',
        help='It adds an option on invoices to verify the afip authorization '
        'data (for documents with CAE, CAI or CAEA).\n'
        'If you choose required, then on supplier invoices, verification is '
        'mandatory before invoice validation',
    )

    @api.model
    def _get_environment_type(self):
        """
        Function to define homologation/production environment
        First it search for a paramter "afip.ws.env.type" if exists and:
        * is production --> production
        * is homologation --> homologation
        Else
        Search for 'server_mode' parameter on conf file. If that parameter is:
        * 'test' or 'develop' -->  homologation
        * other or no parameter -->  production
        """
        _logger.debug('**********_get_environment_type*********')
        parameter_env_type = self.env[
            'ir.config_parameter'
        ].get_param('afip.ws.env.type')
        _logger.debug('1 parameter_env_type = %s' % str(parameter_env_type))
        if parameter_env_type == 'production':
            environment_type = 'production'
        elif parameter_env_type == 'homologation':
            environment_type = 'homologation'
        else:
            server_mode = tools.config.get('server_mode')
            _logger.debug('1 server_mode: %s' % str(server_mode))
            if not server_mode or server_mode == 'production':
                environment_type = 'production'
            else:
                environment_type = 'homologation'
            _logger.debug('2 server_mode: %s' % str(server_mode))
        _logger.debug('2 parameter_env_type = %s' % str(parameter_env_type))
        _logger.debug(
            'Running arg electronic invoice on %s mode' % str(environment_type)
        )
        return environment_type

    @api.multi
    def get_key_and_certificate(self, environment_type):
        """
        Funcion que busca para el environment_type definido,
        una clave y un certificado en los siguientes lugares y segun estas
        prioridades:
        * en el conf del server de odoo
        * en registros de esta misma clase
        """
        self.ensure_one()
        pkey = False
        cert = False
        msg = False
        certificate = self.env['afipws.certificate'].search([
            ('alias_id.company_id', '=', self.id),
            ('alias_id.type', '=', environment_type),
            ('state', '=', 'confirmed'),
        ], limit=1)
        if certificate:
            pkey = certificate.alias_id.key
            cert = certificate.crt
            _logger.debug('Using DB certificates')
        # not certificate on bd, we search on odo conf file
        else:
            msg = _('Not confirmed certificate for %s on company %s') % (
                environment_type, self.name)
            pkey_path = False
            cert_path = False
            if environment_type == 'production':
                pkey_path = tools.config.get('afip_prod_pkey_file')
                cert_path = tools.config.get('afip_prod_cert_file')
            else:
                pkey_path = tools.config.get('afip_homo_pkey_file')
                cert_path = tools.config.get('afip_homo_cert_file')
            if pkey_path and cert_path:
                try:
                    if os.path.isfile(pkey_path) and os.path.isfile(cert_path):
                        with open(pkey_path, "r") as pkey_file:
                            pkey = pkey_file.read()
                        with open(cert_path, "r") as cert_file:
                            cert = cert_file.read()
                    msg = 'Could not find %s or %s files' % (
                        pkey_path, cert_path)
                except Exception:
                    msg = 'Could not read %s or %s files' % (
                        pkey_path, cert_path)
                else:
                    _logger.debug('Using odoo conf certificates')
        if not pkey or not cert:
            raise UserError(msg)
        return (pkey, cert)

    @api.multi
    def get_connection(self, afip_ws):
        self.ensure_one()
        _logger.debug('Getting connection for company %s and ws %s' % (
            self.name, afip_ws))
        now = fields.Datetime.now()
        environment_type = self.sudo()._get_environment_type()

        connection = self.connection_ids.search([
            ('type', '=', environment_type),
            ('generationtime', '<=', now),
            ('expirationtime', '>', now),
            ('afip_ws', '=', afip_ws),
            ('company_id', '=', self.id),
        ], limit=1)
        if not connection:
            connection = self._create_connection(afip_ws, environment_type)
        return connection

    @api.multi
    def _create_connection(self, afip_ws, environment_type):
        """
        This function should be called from get_connection. Not to be used
        directyl
        TODO ver si podemos usar metodos de py3afipws para esto
        """
        self.ensure_one()
        _logger.debug(
            'Creating connection for company %s, environment type %s and ws '
            '%s' % (self.name, environment_type, afip_ws)
        )
        login_url = self.env['afipws.connection'].get_afip_login_url(
            environment_type)
        pkey, cert = self.get_key_and_certificate(environment_type)
        # because py3afipws wsaa loos for "BEGIN RSA PRIVATE KEY" we change key
        if pkey.startswith("-----BEGIN PRIVATE KEY-----"):
            pkey = pkey.replace(" PRIVATE KEY", " RSA PRIVATE KEY")
        auth_data = self.authenticate(
            afip_ws, cert, pkey, wsdl=login_url)
        auth_data.update({
            'company_id': self.id,
            'afip_ws': afip_ws,
            'type': environment_type,
        })
        _logger.debug("Successful Connection to AFIP.")
        return self.connection_ids.create(auth_data)

    @api.model
    def authenticate(self, service, certificate, private_key, force=False,
                     cache="", wsdl="", proxy=""):
        """
        Call AFIP Authentication webservice to get token & sign or error
        message
        """
        # import AFIP webservice authentication helper:
        from py3afipws.wsaa import WSAA
        # create AFIP webservice authentication helper instance:
        wsaa = WSAA()
        # raise python exceptions on any failure
        wsaa.LanzarExcepciones = True

        # five hours
        DEFAULT_TTL = 60 * 60 * 5

        # make md5 hash of the parameter for caching...
        fn = "%s.xml" % hashlib.md5(
            str(service + certificate + private_key).encode('utf8')
        ).hexdigest()
        if cache:
            fn = os.path.join(cache, fn)
        else:
            fn = os.path.join(wsaa.InstallDir, "cache", fn)

        try:
            # read the access ticket (if already authenticated)
            if not os.path.exists(fn) or \
               os.path.getmtime(fn) + (DEFAULT_TTL) < time.time():
                # access ticket (TA) outdated, create new access request
                # ticket (TRA)
                tra = wsaa.CreateTRA(service=service, ttl=DEFAULT_TTL)
                # cryptographically sing the access ticket
                _logger.debug('tra___: ' + str(tra))
                _logger.debug('certificate___: ' + str(certificate))
                _logger.debug('private_key___: ' + str(private_key))
                cms = wsaa.SignTRA(tra, certificate, private_key)
                # connect to the webservice:
                wsaa.Conectar(cache, wsdl, proxy)
                # call the remote method
                _logger.debug('___________WSAA.LOGINCMS_____________ ')
                _logger.debug('CMS:  ' + str(cms))
                ta = wsaa.LoginCMS(cms)
                _logger.debug('____________WSAA.LOGINCMS PASSED__________ ')
                if not ta:
                    raise RuntimeError()
                # write the access ticket for further consumption
                open(fn, "w").write(ta)
            else:
                # get the access ticket from the previously written file
                ta = open(fn, "r").read()
            # analyze the access ticket xml and extract the relevant fields
            _logger.debug("___TA___: " + str(ta))
            wsaa.AnalizarXml(xml=ta)

            token = wsaa.ObtenerTagXml("token")
            sign = wsaa.ObtenerTagXml("sign")
            expirationTime = wsaa.ObtenerTagXml("expirationTime")
            generationTime = wsaa.ObtenerTagXml("generationTime")
            uniqueId = wsaa.ObtenerTagXml("uniqueId")
        except:
            token = sign = None
            if wsaa.Excepcion:
                # get the exception already parsed by the helper
                err_msg = wsaa.Excepcion
            else:
                # avoid encoding problem when reporting exceptions to the user:
                err_msg = traceback.format_exception_only(
                    sys.exc_type, sys.exc_value)[0]
            raise UserError(
                _('Could not connect. This is the what we received: %s') % (
                    err_msg)
            )
        return {
            'uniqueid': uniqueId,
            'generationtime': generationTime,
            'expirationtime': expirationTime,
            'token': token,
            'sign': sign,
        }

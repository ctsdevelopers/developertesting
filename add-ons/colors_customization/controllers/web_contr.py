# -*- coding: utf-8 -*-

import functools

from io import StringIO


import werkzeug.utils
import werkzeug.wrappers


import odoo

from odoo import http
from odoo.addons.web.controllers.main import Binary, Home, db_monodb, ensure_db
from odoo.http import request
from odoo.modules import get_module_resource


def db_info():
    version_info = odoo.service.common.exp_version()
    return {
        'server_version': version_info.get('server_version'),
        'server_version_info': version_info.get('server_version_info'),
    }


class HomeStyle(Home):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        ensure_db()
        if not request.session.uid:
            return werkzeug.utils.redirect('/web/login', 303)
        if kw.get('redirect'):
            return werkzeug.utils.redirect(kw.get('redirect'), 303)

        request.uid = request.session.uid
        theme_id = request.env['res.users'].browse(request.uid).company_color_theme
        theme_data = False
        if theme_id:
            if theme_id.footer_color:
                footer_color = theme_id.footer_color
            else:
                footer_color = '#a24689'

            if theme_id.footer_url:
                footer_url = theme_id.footer_url
            else:
                footer_url = '/web'

            theme_data = {
                'footer_text': theme_id.footer_text,
                'footer_url': footer_url,
                'url_favicon': theme_id.url_favicon,
                'footer_color': footer_color,
                'meta_title': theme_id.meta_title,
            }
        else:
            theme_data = {
                'footer_text': False,
                'footer_url': False,
                'url_favicon': False,
                'footer_color': False,
                'meta_title': False,
            }

        context = request.env['ir.http'].webclient_rendering_context()
        context['theme_data'] = theme_data

        return request.render('web.webclient_bootstrap', qcontext=context)


class Binary_ITL(Binary):

    @http.route([
        '/web/binary/company_logo',
        '/logo',
        '/logo.png',
    ], type='http', auth="none", cors="*")
    def company_logo(self, dbname=None, **kw):
        imgname = 'placeholder.png'
        placeholder = functools.partial(get_module_resource, 'web', 'static', 'src', 'img')
        dbname = request.session and request.session.db or db_monodb()
        uid = request.session and request.session.uid or odoo.SUPERUSER_ID

        if not dbname:
            response = http.send_file(placeholder(imgname))
        else:
            try:
                # create an empty registry
                registry = odoo.modules.registry.Registry(dbname)
                with registry.cursor() as cr:
                    cr.execute("""
                        SELECT c.logo_web, c.write_date
                        FROM res_users u
                            LEFT JOIN res_company c ON c.id = u.company_id
                        WHERE u.id = %s
                    """, (uid))
                    row = cr.fetchone()
                    if row and row[0]:
                        image_data = StringIO(str(row[0]).decode('base64'))
                        response = http.send_file(image_data, filename=imgname, mtime=row[1])
                    else:
                        response = http.send_file(placeholder('placeholder.png'))
            except Exception:
                response = http.send_file(placeholder(imgname))

        return response

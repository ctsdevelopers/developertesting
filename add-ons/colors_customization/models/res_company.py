# -*- coding: utf-8 -*-

from odoo import fields, models, _


class res_company(models.Model):
    _inherit = 'res.company'

    user_own_theme = fields.Boolean(
        u'Allow users to change an interface theme through preferences',
        default=True,
    )
    custom_email_footer = fields.Char(
        u'Footer Text',
        translate=True,
        help=_(u"""
            Some marketing info attached to all emails: e.g. website instead of standard 'sent by ... using Odoo'
            Leave it empty to send emails without footers at all.
            You may use html tags here, including urls.
        """),
    )
    footer_link = fields.Char(
        u'Object Link in Footer',
        translate=True,
        help=_(u"""
            A link to the object where this email comes form: use it instead of standard 'access directly ...''
            Leave it empty no to add url at all
            Put here text in a format 'Some text * Some Text'.
            E.g. 'Access * ' which would be translated in 'Access Lead Super'.
            Be cautious: do not remove *. Otherwise, link would not be added to emails.
        """),
    )

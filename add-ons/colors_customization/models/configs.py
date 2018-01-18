# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class interface_conf(models.TransientModel):
    _name = 'interface.conf'
    _description = 'Interface Settings'

    company_id = fields.Many2one(
        'res.company',
        string=u'Company',
        required=True,
        default=lambda self: self.env.user.company_id or False,
    )
    user_own_theme = fields.Boolean(related='company_id.user_own_theme')

    @api.multi
    def return_template(self):
        return {
            'name': _('Mail Basic Style'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('mail.email_template_form').id,
            'res_model': 'mail.template',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self.env.ref('mail.mail_template_data_notification_email_default').id,
        }

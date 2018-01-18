# -*- coding: utf-8 -*-

from odoo import fields, models


class res_users(models.Model):
    _inherit = 'res.users'

    def __init__(self, pool, cr):
        super(res_users, self).__init__(pool, cr)
        self.SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        self.SELF_WRITEABLE_FIELDS.extend(['company_color_theme'])

    def get_default_theme(self):
        themes = self.env['colors.customization.theme'].search([('default_for_new_users', '=', True)])
        if themes and len(themes) > 0:
            theme = themes[0].id
        else:
            theme = themes
        return theme

    company_color_theme = fields.Many2one(
        'colors.customization.theme',
        u"Interface theme",
        default=lambda self: self.get_default_theme(),
    )
    user_own_theme = fields.Boolean(related='company_id.user_own_theme')

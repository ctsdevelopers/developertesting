# -*- coding: utf-8 -*-

from odoo import models, api


class Waranty(models.AbstractModel):
    _inherit = 'publisher_warranty.contract'

    @api.model
    def update_notification(self):
        return True

# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools


class color_theme(models.Model):
    _name = 'colors.customization.theme'

    def _get_properties(self):
        return [
            ('nav.navbar-inverse', 'background-color', self.navbar_color),
            ('nav.navbar-inverse', 'border-color', self.navbar_border_color),
            ('.navbar-inverse .navbar-nav > li > a', 'color', self.menu_font_color),
            (
                '.navbar-inverse .navbar-nav > .active > a,  .navbar-inverse .navbar-nav > .active > a:focus',
                'color', self.navbar_active_item_font_color
            ),
            ('.navbar-inverse .navbar-nav > li.active > a', 'background-color', self.menu_active_item_color),
            ('.navbar-inverse .navbar-nav > li > a:hover', 'color', self.navbar_hover_font_color),
            ('.navbar-inverse .navbar-nav > li > a:hover', 'background-color', self.navbar_hover_background_color),
            ('.o_sub_menu', 'background', self.left_bar_color),
            ('.nav-pills li > a', 'color', self.left_bar_font_color),
            ('.oe_secondary_menu_section', 'color', self.left_bar_category_font_color),
            ('.oe_secondary_menu_section > .oe_menu_leaf > .oe_menu_text', 'color', self.left_bar_menu_text),
            ('.nav-pills > li.active > a', 'background-color', self.left_bar_active_item_color),
            ('.nav-pills > li.active > a', 'color', self.left_bar_active_item_font_color),
            ('.nav-pills > li > a:hover', 'color', self.left_bar_hover_font_color),
            ('.nav-pills > li > a:hover', 'background-color', self.left_bar_hover_background_color),
            ('.o_control_panel', 'background-color', self.header_table_color),
            ('.o_control_panel', 'background-image', self.webkit_gradient),
            ('.o_control_panel', 'background-image', self.linear_gradient),
            ('.o_control_panel', 'background-image', self.moz_gradient),
            ('.o_control_panel', 'background-image', self.ms_gradient),
            ('.o_control_panel', 'background-image', self.lin_gradient),
            ('.o_control_panel', 'background-image', self.gradient_bot),
            ('.o_mail_chat_sidebar', 'background-color', self.navbar_color),
            ('.o_mail_chat_sidebar', 'border-color', self.navbar_border_color),
            ('.o_mail_chat_sidebar', 'color', self.menu_font_color),
            ('.o_mail_chat_sidebar .o_mail_chat_channel_item.o_active', 'color', self.navbar_active_item_font_color),
            (
                '.o_mail_chat_sidebar .o_mail_chat_channel_item.o_active',
                'background-color', self.menu_active_item_color
            ),
            ('.o_mail_chat_sidebar .o_mail_chat_channel_item:hover', 'color', self.navbar_hover_font_color),
            ('.o_mail_chat_sidebar .o_mail_chat_channel_item:hover',
             'background-color', self.navbar_hover_background_color),
            ('.o_mail_sidebar_title h4.o_mail_open_channels:hover', 'color', self.menu_font_color),
            ('.breadcrumb', 'background-color', 'rgba(0, 0, 0, 0);'),
        ]

    def _build_rule(self, selector, prop, value):
        return "{s} {{ {p}: {v} !important;}}\n".format(s=selector, p=prop, v=value)

    @api.depends(
        'navbar_color', 'navbar_border_color',
        'menu_font_color', 'left_bar_color',
        'menu_active_item_color', 'left_bar_menu_text',
        'navbar_hover_font_color', 'navbar_hover_background_color',
        'left_bar_font_color', 'left_bar_category_font_color',
        'left_bar_active_item_color', 'navbar_active_item_font_color',
        'left_bar_active_item_font_color',
        'left_bar_hover_font_color', 'left_bar_hover_background_color',
        'header_table_color', 'header_table_color_2',
    )
    def _compute_css(self):
        result = ''
        for field in self._get_properties():
            result += self._build_rule(field[0], field[1], field[2])
        self.css = result

    @api.multi
    def _compute_header_gradient_webkit(self):
        self.ensure_one()
        if self.header_table_color and self.header_table_color_2:
            self.webkit_gradient = '-webkit-gradient(linear, left top, left bottom, from(' + \
                self.header_table_color + '), to(' + self.header_table_color_2 + '))'
            self.linear_gradient = '-webkit-linear-gradient(top, ' + \
                self.header_table_color + ', ' + self.header_table_color_2 + ')'
            self.moz_gradient = '-moz-linear-gradient(top,' + self.header_table_color + \
                ', ' + self.header_table_color_2 + ')'
            self.ms_gradient = '-ms-linear-gradient(top,' + self.header_table_color + \
                ', ' + self.header_table_color_2 + ')'
            self.lin_gradient = '-o-linear-gradient(top,' + self.header_table_color + \
                ', ' + self.header_table_color_2 + ')'
            self.gradient_bot = 'linear-gradient(to bottom,' + self.header_table_color + \
                ', ' + self.header_table_color_2 + ')'
        else:
            self.webkit_gradient = self.linear_gradient = self.moz_gradient = self.ms_gradient = \
                self.lin_gradient = self.gradient_bot = False

    @api.multi
    def _inverse_default_theme(self):
        self.ensure_one()
        if self.default_for_new_users:
            for theme in self.search([('id', '!=', self.id)]):
                theme.default_for_new_users = False

    @api.multi
    @api.depends('image')
    def _compute_image(self):
        self.ensure_one()
        images = tools.image_get_resized_images(self.image)
        self.image_small = images.get('image_small')
        self.image_medium = images.get('image_medium')

    @api.multi
    @api.depends('image_small')
    def _compute_image_small_url(self):
        self.ensure_one()
        self.url_favicon = 'web/image?model=colors.customization.theme&id=' + str(self.id) + '&field=image_small'

    name = fields.Char(
        u'Name',
        required=True,
        translate=True,
    )
    css = fields.Char(
        u'CSS',
        compute='_compute_css',
        store=True,
    )

    navbar_color = fields.Char(u'Background Color')
    navbar_border_color = fields.Char(u'Border Color')
    navbar_active_item_font_color = fields.Char(u'Active Item Font Color')
    menu_font_color = fields.Char(u'Font Color')
    menu_active_item_color = fields.Char(u'Active Item Background Color')
    navbar_hover_font_color = fields.Char(u'Hover Font Color')
    navbar_hover_background_color = fields.Char(u'Hover Background Color')

    left_bar_color = fields.Char(u'Background Color')
    left_bar_menu_text = fields.Char(u'Individual Menu Color')

    left_bar_font_color = fields.Char(u'Sub Menu Color')
    left_bar_category_font_color = fields.Char(u'Main Menu Color')
    left_bar_active_item_font_color = fields.Char(u'Active Item Font Color')
    left_bar_active_item_color = fields.Char(u'Active Item Background Color')
    left_bar_hover_font_color = fields.Char(u'Hover Font Color')
    left_bar_hover_background_color = fields.Char(u'Hover Background Color')

    header_table_color = fields.Char(u'Header Section Background (Gradient)')
    header_table_color_2 = fields.Char(u'Header Section Background 2')
    webkit_gradient = fields.Char(
        u'Gradient',
        compute='_compute_header_gradient_webkit',
    )
    linear_gradient = fields.Char(
        u'Gradient',
        compute='_compute_header_gradient_webkit',
    )
    moz_gradient = fields.Char(
        u'Gradient',
        compute='_compute_header_gradient_webkit',
    )
    ms_gradient = fields.Char(
        u'Gradient',
        compute='_compute_header_gradient_webkit',
    )
    lin_gradient = fields.Char(
        u'Gradient',
        compute='_compute_header_gradient_webkit',
    )
    gradient_bot = fields.Char(
        u'Gradient',
        compute='_compute_header_gradient_webkit',
    )

    users = fields.One2many(
        'res.users',
        'company_color_theme',
        string=u'Users',
        help=_(u'Only one theme may be specified to a user'),
    )
    default_for_new_users = fields.Boolean(
        string=u'Default',
        inverse='_inverse_default_theme',
        help=_(u'This theme would be applied to new users. There could be only one default theme'),
    )
    image = fields.Binary(u'Favicon')
    image_medium = fields.Binary(
        compute='_compute_image',
        string=u'Image Medium',
        store=True,
    )
    image_small = fields.Binary(
        compute='_compute_image',
        string=u'Image Small',
        store=True,
    )
    url_favicon = fields.Char(compute='_compute_image_small_url')
    footer_text = fields.Char(
        u'Footer',
        help=_(u'Leave it empty to delete a footer at all'),
        translate=True,
    )
    footer_url = fields.Char(
        u'URL',
        help=_(u'Use http or https to have an absolute url'),
    )
    footer_color = fields.Char(u'Color')

    remove_menu_preferences = fields.Boolean(
        u'Hide Preferences',
        help=_(u'From the user menu'),
        default=False,
    )
    remove_menu_account = fields.Boolean(
        u'Hide Account',
        help=_(u'From the user menu'),
        default=True,
    )
    remove_menu_help = fields.Boolean(
        u'Hide Support',
        help=_(u'From the user menu'),
        default=True,
    )
    remove_menu_documentation = fields.Boolean(
        u'Hide Documentation',
        help=_(u'From the user menu'),
        default=False,
    )
    meta_title = fields.Char(
        u'Page Title',
        help=_(u'Instead of Odoo'),
    )

    _order = 'id'

    @api.multi
    def assign_to_all_users(self):
        self.ensure_one()
        for user in self.env['res.users'].search([]):
            user.company_color_theme = self

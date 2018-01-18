odoo.define('colors_customization.menu', function(require) {
    "use strict";

    var core = require('web.core');
    var framework = require('web.framework');
    var session = require('web.session');
    var concurrency = require('web.concurrency');
    var rpc = require("web.rpc");
    var UserMenu = require('web.UserMenu');
    var WebClient = require('web.WebClient');
    var QWeb = core.qweb;

    UserMenu.include({
        start: function() {
            var res = this._super.apply(this, arguments);
            var self = this;

            var fct = function() {
                if (!session.uid)
                    return;

                rpc.query({
                    model: 'res.users',
                    method: 'read',
                    args: [self.getSession().uid],
                    kwargs: {
                        fields: ['name'],
                    },
                }).then(function(user) {
                    rpc.query({
                        model: 'colors.customization.theme',
                        method: 'search_read',
                        kwargs: {
                            fields: [
                                'name', 'remove_menu_account', 'remove_menu_preferences',
                                'remove_menu_help', 'remove_menu_documentation'
                            ],
                            domain: [
                                ['users', '=', user[0].id]
                            ],
                            limit: 1,
                        },
                    }).then(function(theme) {
                        if (theme.length > 0) {
                            var $account_menu = self.$el.find("a[data-menu]");
                            $account_menu.each(function(index, menu_obj) {
                                if (menu_obj.getAttribute('data-menu') == 'account') {
                                    if (theme[0].remove_menu_account) {
                                        menu_obj.remove();
                                    };
                                };
                                if (menu_obj.getAttribute('data-menu') == 'settings') {
                                    if (theme[0].remove_menu_preferences) {
                                        menu_obj.remove();
                                    };
                                };
                                if (menu_obj.getAttribute('data-menu') == 'support') {
                                    if (theme[0].remove_menu_help) {
                                        menu_obj.remove();
                                    };
                                };
                                if (menu_obj.getAttribute('data-menu') == 'documentation') {
                                    if (theme[0].remove_menu_documentation) {
                                        menu_obj.remove();
                                    };
                                };

                            });
                        }
                    });
                });

                return self.alive(
                        rpc.query({
                            model: 'res.users',
                            method: 'read',
                            args: [self.getSession().uid],
                            kwargs: {
                                fields: ['name', "company_id"],
                            },
                        })
                    )
                    .then(function(res) {
                        var topbar_name = res[0].name;
                        if (session.debug)
                            topbar_name = _.str.sprintf("%s (%s)", topbar_name, session.db);
                        if (res[0].company_id[0] > 1)
                            topbar_name = _.str.sprintf("%s (%s)", topbar_name, res[0].company_id[1]);
                        self.$el.find('.oe_topbar_name').text(topbar_name);
                        if (!session.debug) {
                            topbar_name = _.str.sprintf("%s (%s)", topbar_name, session.db);
                        }
                        core.bus.trigger('resize'); // Re-trigger the reflow logic
                    });
            };
            fct();
        },
    });

    WebClient.include({
        show_application: function() {
            this._super.apply(this, arguments);
            this._current_state = null;
            this.menu_dm = new concurrency.DropMisordered();
            this.action_mutex = new concurrency.Mutex();
            this.set('title_part', {
                "zodoo": ""
            });
            var self = this;

            session.rpc("/web/session/get_session_info", {}).then(function(result) {
                if (result.uid) {
                    rpc.query({
                            model: 'res.users',
                            method: 'read',
                            args: [self.getSession().uid],
                            kwargs: {
                                fields: ['name'],
                            },
                        })
                        .then(function(user) {
                            rpc.query({
                                    model: 'colors.customization.theme',
                                    method: 'search_read',
                                    kwargs: {
                                        fields: ['name', 'meta_title'],
                                        domain: [
                                            ['users', '=', user[0].id]
                                        ],
                                        limit: 1,
                                    },
                                })
                                .then(function(theme) {
                                    if (theme.length > 0) {
                                        if (theme[0].meta_title) {
                                            self.set('title_part', {
                                                "zodoo": theme[0].meta_title
                                            });
                                        };
                                    };
                                });
                        });
                }
            });
        },
    });

});

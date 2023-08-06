# -*- coding: utf-8 -*-
'''
udata-koumoul

Theme for Koumoul's demo opendata portal
'''


from udata.app import nav
from udata.i18n import lazy_gettext as _
from udata import theme

nav.Bar('footer_documentation', [
    nav.Item(_('Catalogue de données'), None, url='https://github.com/opendatateam/udata/', items=[
        nav.Item(_('API'), 'apidoc.swaggerui'),
        nav.Item(_('Documentation technique'), None, url='https://udata.readthedocs.io/'),
    ]),
    nav.Item(_('Diffusion de données'), None, url='https://github.com/koumoul-dev/data-fair/', items=[
        nav.Item(_('Manuel utilisateur'), None, url='https://koumoul-dev.github.io/data-fair/user-guide'),
        nav.Item(_('Installation'), None, url='https://koumoul-dev.github.io/data-fair/install'),
        nav.Item(_('Contribuer à l\'écosystème'), None, url='https://koumoul-dev.github.io/data-fair/interoperate'),
    ]),
    nav.Item(_('Conditions d\'utilisation'), 'site.terms'),
])

default_menu = nav.Bar('default_menu', [
    nav.Item(_('Organizations'), 'organizations.list'),
    nav.Item(_('Datasets'), 'datasets.list'),
    nav.Item(_('Reuses'), 'reuses.list')
])

theme.menu(default_menu)

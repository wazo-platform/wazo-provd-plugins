common = {}

execfile_('common.py', common)

MODELS = [
    'GXP2135',
]

VERSION = '1.0.11.79'


class GrandstreamPlugin(common['BaseGrandstreamPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common['BaseGrandstreamPgAssociator'](MODELS, VERSION)


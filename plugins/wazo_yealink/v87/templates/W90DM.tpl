{% extends 'base-dect.tpl' -%}

static.auto_provision.pnp_enable = 0
static.auto_provision.custom.protect = 1
static.auto_provision.handset_configured.enable = 1

custom.handset.date_format = {{ XX_handset_lang|d('%NULL%') }}
custom.handset.screen_saver.enable = 0
custom.handset.silent_charging = 0

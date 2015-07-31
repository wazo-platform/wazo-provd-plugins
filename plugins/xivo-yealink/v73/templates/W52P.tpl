{% extends 'base.tpl' -%}

{% block model_specific_parameters -%}
auto_provision.handset_configured.enable = 1

custom.handset.date_format = 2
custom.handset.language = {{ XX_handset_lang|d('%NULL%') }}
custom.handset.screen_saver.enable = 0
{% endblock %}

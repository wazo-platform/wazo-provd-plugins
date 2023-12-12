{% extends 'base.tpl' -%}

{% if XX_handsets_fw -%}
{% for handset, fw_file in XX_handsets_fw.items() -%}
over_the_air.url.{{ handset }} = {{ XX_server_url }}/firmware/{{ fw_file }}
{% endfor -%}
over_the_air.handset_tip = 0
{%- endif %}

{% block model_specific_parameters -%}
gui_lang.url = {{ XX_server_url }}/lang/T41S-T42S-T53W-T53/004.GUI.French.lang
{% endblock %}

{% extends 'base.tpl' -%}
{% for line_no, line in XX_sip_lines.iteritems() -%}
{% if line -%}
account.{{ line_no }}.codec.g722.enable = 1
account.{{ line_no }}.codec.g722_1c_48kpbs.enable = 0
account.{{ line_no }}.codec.g722_1c_32kpbs.enable = 0
account.{{ line_no }}.codec.g722_1c_24kpbs.enable = 0
account.{{ line_no }}.codec.g722_1_24kpbs.enable = 0
{% endif %}
{% endfor %}

{% block model_specific_parameters -%}
gui_lang.url = http://{{ ip }}:{{ http_port }}/lang/T58-CP960/003.GUI.French.lang
{% endblock %}

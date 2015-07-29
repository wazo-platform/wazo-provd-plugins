{% extends 'base.tpl' -%}

{% block sip_line_label %}
account.{{ line['XX_line_no'] }}.label = {{ line['display_name'] }} {{ line['number'] }}
{% endblock %}

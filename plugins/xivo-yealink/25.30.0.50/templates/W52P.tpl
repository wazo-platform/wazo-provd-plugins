{% extends 'base.tpl' -%}

{% block sip_servers %}
account.{{ line['XX_line_no'] }}.sip_server_host = {{ line['proxy_ip'] }}
account.{{ line['XX_line_no'] }}.sip_server_port = {{ line['proxy_port'] }}
{% endblock %}

{% block suffix %}
{% for line in sip_lines.itervalues() %}
handset.{{ line['XX_line_no'] }}.name = {{ line['display_name'] }}
handset.{{ line['XX_line_no'] }}.incoming_lines = {{ line['XX_line_no'] }}
handset.{{ line['XX_line_no'] }}.dial_out_default_line = {{ line['XX_line_no'] }}
handset.{{ line['XX_line_no'] }}.dial_out_lines = {{ line['XX_line_no'] }}
{% endfor -%}
{% endblock %}

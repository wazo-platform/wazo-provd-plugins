{% extends 'base.tpl' -%}

{% block sip_servers %}
account.{{ line['XX_line_no'] }}.sip_server.1.address = {{ line['proxy_ip'] }}
account.{{ line['XX_line_no'] }}.sip_server.1.port = {{ line['proxy_port'] }}
account.{{ line['XX_line_no'] }}.sip_server.2.address = {{ line['backup_proxy_ip'] }}
account.{{ line['XX_line_no'] }}.sip_server.2.port = {{ line['backup_proxy_port'] }}
{% endblock %}

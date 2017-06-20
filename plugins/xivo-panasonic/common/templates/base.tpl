# Panasonic SIP Phone Standard Format File #

{# VLAN settings -#}
{% if vlan_enabled -%}
VLAN_ENABLE="Y"
VLAN_ID_IP_PHONE="{{ vlan_id }}"
{% if vlan_pc_port_id is defined -%}
VLAN_ID_PC="{{ vlan_pc_port_id }}"
{% endif -%}
{% else -%}
VLAN_ENABLE="N"
{% endif -%}


{# NTP settings -#}
NTP_ADDR="{{ ntp_ip }}"

{# Syslog settings -#}
{% if syslog_enabled -%}
SYSLOG_ADDR="{{ syslog_ip }}"
SYSLOG_PORT="{{ syslog_port }}"
{% endif -%}


{# SIP per-line settings -#}
{% for line_no, line in sip_lines.iteritems() %}
PHONE_NUMBER_{{ line_no }}="{{ line['number'] }}"
DISPLAY_NAME_{{ line_no }}="{{ line['display_name'] }}"
VM_NUMBER_{{ line_no }}="{{ line['voicemail'] }}"
SIP_URI_{{ line_no }}="sip:{{ line['auth_username'] }}@{{ line['registrar_ip'] }}"
SIP_PRXY_ADDR_{{ line_no }}="{{ line['proxy_ip'] }}"
SIP_2NDPROXY_ADDR_{{ line_no }}="{{ line['backup_proxy_ip'] }}"
SIP_RGSTR_ADDR_{{ line_no }}="{{ line['registrar_ip'] }}"
SIP_2NDRGSTR_ADDR_{{ line_no }}="{{ line['backup_registrar_ip'] }}"
SIP_AUTHID_{{ line_no }}="{{ line['auth_username'] }}"
SIP_PASS_{{ line_no }}="{{ line['password'] }}"
{% endfor -%}

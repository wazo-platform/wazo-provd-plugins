{# DNS settings #}
{% if dns_enabled -%}
dns1: {{ dns_ip }}
{% endif -%}

{# Syslog settings -#}
{% if syslog_enabled -%}
log server ip: {{ syslog_ip }}
log server port: {{ syslog_port }}
log module linemgr: {{ XX_log_level }}
log module user interface: {{ XX_log_level }}
log module sip: {{ XX_log_level }}
log module ept: {{ XX_log_level }}
log module ind: {{ XX_log_level }}
log module kbd: {{ XX_log_level }}
log module net: {{ XX_log_level }}
log module provis: {{ XX_log_level }}
log module rtpt: {{ XX_log_level }}
log module snd: {{ XX_log_level }}
log module stun: {{ XX_log_level }}
{% endif -%}

{# VLAN settings -#}
{% if vlan_enabled -%}
tagging enabled: 1
vlan id: {{ vlan_id }}
{% if vlan_priority is defined -%}
priority non-ip: {{ vlan_priority }}
{% endif -%}
{% if vlan_pc_port_id is defined -%}
vlan id port 1: {{ vlan_pc_port_id }}
{% else -%}
vlan id port 1: 4095
{% endif -%}
{% else -%}
tagging enabled: 0
{% endif -%}

{# NTP settings -#}
{% if ntp_enabled -%}
time server disabled: 0
time server1: {{ ntp_ip }}
{% else -%}
time server disabled: 1
{% endif -%}

{% if admin_password -%}
admin password: {{ admin_password }}
{% endif -%}
{% if user_password -%}
user password: {{ user_password }}
{% endif -%}

{{ XX_timezone }}

{% if XX_locale -%}
language: 1
language 1: i18n/{{ XX_locale[0] }}
tone set: {{ XX_locale[1] }}
input language: {{ XX_locale[2] }}
{% endif -%}

{# SIP global settings -#}
{# DTMF global settings-#}
{% if XX_out_of_band_dtmf -%}
sip out-of-band dtmf: {{ XX_out_of_band_dtmf }}
{% endif -%}
{% if XX_dtmf_method -%}
sip dtmf method: {{ XX_dtmf_method }}
{% endif -%}

{% if sip_subscribe_mwi is defined -%}
sip explicit mwi subscription: {{ sip_subscribe_mwi|int }}
{% endif -%}

{% if XX_transport_proto -%}
sip transport protocol: {{ XX_transport_proto }}
{% endif -%}

{% if XX_trusted_certificates -%}
sips trusted certificates: {{ XX_trusted_certificates }}
{% endif -%}

{# SIP per-line settings -#}
{% for line_no, line in sip_lines.iteritems() %}
sip line{{ line_no }} proxy ip: {{ line['proxy_ip'] }}
sip line{{ line_no }} proxy port: {{ line['proxy_port'] }}
sip line{{ line_no }} backup proxy ip: {{ line['backup_proxy_ip'] }}
sip line{{ line_no }} backup proxy port: {{ line['backup_proxy_port'] }}
sip line{{ line_no }} registrar ip: {{ line['registrar_ip'] }}
sip line{{ line_no }} registrar port: {{ line['registrar_port'] }}
sip line{{ line_no }} backup registrar ip: {{ line['backup_registrar_ip'] }}
sip line{{ line_no }} backup registrar port: {{ line['backup_registrar_port'] }}
sip line{{ line_no }} user name: {{ line['username'] }}
sip line{{ line_no }} auth name: {{ line['auth_username'] }}
sip line{{ line_no }} password: {{ line['password'] }}
sip line{{ line_no }} display name: {{ line['display_name'] }}
sip line{{ line_no }} screen name: {{ line['display_name'] }}
{% if line['number'] -%}
sip line{{ line_no }} screen name 2: {{ line['number'] }}
{% endif -%}
sip line{{ line_no }} dtmf method: {{ line['XX_dtmf_method'] }}
sip line{{ line_no }} srtp mode: {{ line['XX_srtp_mode'] }}
{% if line['voicemail'] -%}
sip line{{ line_no }} vmail: {{ line['voicemail'] }}
{% endif -%}
{% endfor -%}

{% if exten_pickup_call -%}
directed call pickup prefix: {{ exten_pickup_call }}
{% endif -%}

{{ XX_parking }}

{{ XX_fkeys }}


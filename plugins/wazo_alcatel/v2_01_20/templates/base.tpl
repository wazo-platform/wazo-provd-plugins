# Note that:
# - absent parameters usually means default value
# - parameters with 'key=' also means default value

[dns]
dns_addr={{ XX_dns_addr }}


[sip]
domain_name={{ sip_proxy_ip }}
proxy_addr={{ sip_proxy_ip }}
proxy_port={% if sip_proxy_port %}{{ sip_proxy_port }}{% endif %}
registrar_addr={{ sip_registrar_ip }}
registrar_port={% if sip_registrar_port %}{{ sip_registrar_port }}{% endif %}
outbound_proxy_addr={% if sip_outbound_proxy_ip %}{{ sip_outbound_proxy_ip }}{% endif %}
outbound_proxy_port={% if sip_outbound_proxy_port %}{{ sip_outbound_proxy_port }}{% endif %}

proxy2_addr={% if sip_backup_proxy_ip %}{{ sip_backup_proxy_ip }}{% endif %}
proxy2_port={% if sip_backup_proxy_port %}{{ sip_backup_proxy_port }}{% endif %}

registrar2_addr={% if sip_backup_registrar_ip %}{{ sip_backup_registrar_ip }}{% endif %}
registrar2_port={% if sip_backup_registrar_port %}{{ sip_backup_registrar_port }}{% endif %}

sip_transport_mode={{ XX_sip_transport_mode }}

authentication_realm={{ sip_proxy_ip }}
authentication_name={{ XX_auth_name }}
authentication_password={{ XX_auth_password }}
user_name={{ XX_user_name }}
display_name={{ XX_display_name }}

voice_mail_uri={{ XX_voice_mail_uri }}
message_waiting_indication_uri={{ XX_mwi_uri }}


[sntp]
sntp_addr={{ XX_sntp_addr }}
timezone={{ XX_timezone }}


[telnet]
telnet_password={{ admin_password }}


[audio]
tone_country={{ XX_tone_country }}
dtmf_type={{ XX_dtmf_type }}


[appl]
admin_password={{ admin_password }}
{{ XX_fkeys }}

{# Note: if you remove a parameter in the MAC configuration file thinking
         that the value in the common configuration file will apply, you
         are wrong. You'll get this behaviour only after changing the name
         of the common configuration file (and updating the .inf file).
-#}

[ipp]
LanguageType={{ XX_language_type }}

[net]
{% if dns_enabled -%}
DNSSrv1={{ dns_ip }}
{% else -%}
DNSSrv1=0.0.0.0
{% endif -%}

{% if vlan_enabled -%}
VLAN=1
{% else -%}
VLAN=0
{% endif %}

[sip]
CallPkupFlg=sc
{% if exten_pickup_call %}
CallPkupSC={{exten_pickup_call}}X
{% endif %}
{% for line_no in range(1, XX_nb_lines + 1) -%}
{% set line_no = line_no|string -%}
{% if line_no in sip_lines -%}
{% set line = sip_lines[line_no] -%}
DisplayNumFlag{{ line_no }}=1
DisplayNum{{ line_no }}={{ line['number'] }}
DisplayName{{ line_no }}={{ line['display_name'] }}
ProxyServerMP{{ line_no }}={{ line['proxy_ip'] or sip_proxy_ip }}
ProxyServerBK{{ line_no }}={{ line['backup_proxy_ip'] or sip_backup_proxy_ip }}
regid{{ line_no }}={{ line['auth_username'] }}
regpwd{{ line_no }}={{ line['password'] }}
RegisterServerMP{{ line_no }}={{ line['registrar_ip'] or sip_registrar_ip }}
RegisterServerBK{{ line_no }}={{ line['backup_registrar_ip'] or sip_backup_registrar_ip }}
TEL{{ line_no }}Number={{ line['username'] }}
TEL0{{ line_no }}Use=1
{% else -%}
DisplayNumFlag{{ line_no }}=0
DisplayNum{{ line_no }}=
DisplayName{{ line_no }}=
ProxyServerMP{{ line_no }}=
ProxyServerBK{{ line_no }}=
regid{{ line_no }}=
regpwd{{ line_no }}=
RegisterServerMP{{ line_no }}=
RegisterServerBK{{ line_no }}=
TEL{{ line_no }}Number=
TEL0{{ line_no }}Use=0
{% endif -%}
{% endfor -%}

TransportFlgMP1={{ XX_transport_flg }}
TransportFlgMP2={{ XX_transport_flg }}
TransportFlgMP3={{ XX_transport_flg }}
TransportFlgMP4={{ XX_transport_flg }}
TransportFlgBK1={{ XX_transport_flg }}
TransportFlgBK2={{ XX_transport_flg }}
TransportFlgBK3={{ XX_transport_flg }}
TransportFlgBK4={{ XX_transport_flg }}

{% if exten_voicemail -%}
VoiceMailTelNum={{ exten_voicemail }}
{% else -%}
VoiceMailTelNum=
{% endif -%}

{% if sip_subscribe_mwi -%}
subscribe_event=1
{% else -%}
subscribe_event=0
{% endif %}

[sys]
config_sn={{ XX_config_sn }}
CountryCode={{ XX_country_code }}
dtmf_mode_flag={{ XX_dtmf_mode_flag }}
Phonebook1_url={{ XX_xivo_phonebook_url }}
Phonebook1_name={{ XX_phonebook_name }}

{{ XX_fkeys }}

{% if user_username is defined -%}
UserID={{ user_username }}
{% endif -%}
{% if user_password is defined -%}
UserPWD={{ user_password }}
{% endif -%}
{% if admin_username is defined -%}
TelnetID={{ admin_username }}
{% endif -%}
{% if admin_password is defined -%}
TelnetPWD={{ admin_password }}
WebPWD={{ admin_password }}
{% endif %}

[qos]
{% if vlan_enabled -%}
VLANid1={{ vlan_id }}
{% if vlan_pc_port_id -%}
VLANid2={{ vlan_pc_port_id }}
{% endif -%}
{% if vlan_priority is defined -%}
VLANTag1={{ vlan_priority }}
{% endif %}
{% endif %}

[ntp]
{% if ntp_enabled -%}
NTPFlag=1
NtpIP={{ ntp_ip }}
{% else -%}
NTPFlag=0
{% endif -%}
NtpZoneNum={{ XX_ntp_zone_num }}

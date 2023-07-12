<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<polycomConfig

device.set="1"

{# VLAN settings -#}
device.net.vlanId.set="1"
{% if vlan_enabled -%}
device.net.vlanId="{{ vlan_id }}"
{% else -%}
device.net.vlanId=""
{% endif -%}

qos.ip.callControl.dscp="46"
qos.ip.rtp.dscp="46"

{# Syslog settings -#}
device.syslog.serverName.set="1"
device.syslog.transport.set="1"
device.syslog.renderLevel.set="1"
{% if syslog_enabled -%}
device.syslog.serverName="{{ syslog_ip }}"
device.syslog.transport="1"
device.syslog.renderLevel="{{ XX_syslog_level }}"
{% else -%}
device.syslog.serverName=""
device.syslog.transport="0"
device.syslog.renderLevel="1"
{% endif -%}

device.auth.localAdminPassword.set="1"
device.auth.localAdminPassword="{{ admin_password|d(9486)|e }}"
device.auth.localUserPassword.set="1"
device.auth.localUserPassword="{{ user_password|d(123)|e }}"

{% if sip_srtp_mode == 'disabled' -%}
sec.srtp.enable="0"
sec.srtp.offer="0"
sec.srtp.require="0"
{% elif sip_srtp_mode == 'preferred' -%}
sec.srtp.enable="1"
sec.srtp.offer="1"
sec.srtp.require="0"
{% elif sip_srtp_mode == 'required' -%}
sec.srtp.enable="1"
sec.srtp.offer="1"
sec.srtp.require="1"
{% endif -%}

{# NTP settings -#}
{% if ntp_enabled -%}
tcpIpApp.sntp.address.overrideDHCP="1"
tcpIpApp.sntp.address="{{ ntp_ip }}"
{% else -%}
tcpIpApp.sntp.address.overrideDHCP="0"
tcpIpApp.sntp.address=""
{% endif -%}

{{ XX_timezone }}

lcl.ml.lang="{{ XX_language }}"

{% if sip_dtmf_mode == 'RTP-in-band' -%}
tone.dtmf.viaRtp="1"
tone.dtmf.rfc2833Control="0"
voIpProt.SIP.dtmfViaSignaling.rfc2976="0"
{% else -%}
tone.dtmf.viaRtp="1"
tone.dtmf.rfc2833Control="1"
voIpProt.SIP.dtmfViaSignaling.rfc2976="0"
{% endif -%}

{% for line_no, line in sip_lines.items() %}
reg.{{ line_no }}.server.1.address="{{ line['proxy_ip'] }}"
reg.{{ line_no }}.server.1.port="{{ line['proxy_port'] }}"
reg.{{ line_no }}.server.1.transport="{{ XX_sip_transport }}"
reg.{{ line_no }}.server.1.expires="3600"
reg.{{ line_no }}.server.1.register="1"
reg.{{ line_no }}.server.1.retryMaxCount="2"
{% if line['backup_proxy_ip'] -%}
reg.{{ line_no }}.server.2.address="{{ line['backup_proxy_ip'] }}"
reg.{{ line_no }}.server.2.port="{{ line['backup_proxy_port'] }}"
reg.{{ line_no }}.server.2.transport="{{ XX_sip_transport }}"
reg.{{ line_no }}.server.2.expires="3600"
{% endif -%}
reg.{{ line_no }}.displayName="{{ line['display_name']|e }}"
reg.{{ line_no }}.label="{{ line['number']|e }}"
reg.{{ line_no }}.address="{{ line['username']|e }}"
reg.{{ line_no }}.auth.userId="{{ line['auth_username']|e }}"
reg.{{ line_no }}.auth.password="{{ line['password']|e }}"
{% if sip_subscribe_mwi -%}
msg.mwi.{{ line_no }}.subscribe="{{ line['number'] }}"
{% else -%}
msg.mwi.{{ line_no }}.subscribe=""
{% endif -%}
msg.mwi.{{ line_no }}.callBackMode="contact"
msg.mwi.{{ line_no }}.callBack="{{ line['voicemail'] }}"
{% endfor -%}

{% if exten_pickup_call -%}
call.directedCallPickupString="{{ exten_pickup_call }}"
{% endif -%}

{{ XX_fkeys }}

{% block remote_phonebook -%}
{% if XX_xivo_phonebook_url -%}
mb.main.home="{{ XX_xivo_phonebook_url|e }}"

softkey.1.enable="1"
softkey.1.action="{{ XX_xivo_phonebook_url|e }}"
softkey.1.label="{{ XX_dict['remote_directory'] }}"
softkey.1.use.idle="1"
{% endif -%}
{% endblock -%}

{% if XX_options['switchboard'] -%}
apps.push.messageType="5"
apps.push.username="xivo_switchboard"
apps.push.password="xivo_switchboard"
call.callWaiting.enable="0"
{% else -%}
apps.push.messageType="0"
apps.push.username=""
apps.push.password=""
call.callWaiting.enable="1"
{% endif %}

{% block model_specific_parameters -%}
{% endblock -%}

/>

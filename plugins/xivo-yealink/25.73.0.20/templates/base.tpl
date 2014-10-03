#!version:1.0.0.1

{% if vlan_enabled -%}
network.vlan.internet_port_enable = 1
network.vlan.internet_port_vid = {{ vlan_id }}
network.vlan.internet_port_priority = {{ vlan_priority|d('%NULL%') }}
{% else -%}
network.vlan.internet_port_enable = 0
network.vlan.internet_port_vid = %NULL%
network.vlan.internet_port_priority = %NULL%
{% endif %}

{% if syslog_enabled -%}
syslog.mode = 1
syslog.server = {{ syslog_ip }}
{% else -%}
syslog.mode = 0
syslog.server = %NULL%
{% endif %}

lang.wui = {{ XX_lang|d('%NULL%') }}

custom.handset.language = {{ XX_handset_lang|d('%NULL%') }}

voice.tone.country = {{ XX_country|d('%NULL%') }}

local_time.ntp_server1 = {{ ntp_ip|d('pool.ntp.org') }}
{% if XX_timezone -%}
{{ XX_timezone }}
{% else -%}
local_time.time_zone = %NULL%
local_time.time_zone_name = %NULL%
local_time.summer_time = %NULL%
{% endif %}

security.user_name.user = {{ user_username|d('user') }}
security.user_name.admin = {{ admin_username|d('admin') }}
security.user_password = {{ user_username|d('user') }}:{{ user_password|d('user') }}
security.user_password = {{ admin_username|d('admin') }}:{{ admin_password|d('admin') }}

{% for account_no in ['1', '2', '3', '4', '5'] -%}
{% set line = sip_lines.get(account_no) -%}
{% if line -%}
account.{{ account_no }}.enable = 1
account.{{ account_no }}.display_name = {{ line['display_name'] }}
account.{{ account_no }}.auth_name = {{ line['auth_username'] }}
account.{{ account_no }}.user_name = {{ line['username'] }}
account.{{ account_no }}.password = {{ line['password'] }}
account.{{ account_no }}.sip_server.1.address = {{ line['proxy_ip'] }}
account.{{ account_no }}.sip_server.1.port = {{ line['proxy_port']|d('%NULL%') }}
account.{{ account_no }}.sip_server.2.address = {{ line['backup_proxy_ip']|d('%NULL%') }}
account.{{ account_no }}.sip_server.2.port = {{ line['backup_proxy_port']|d('%NULL%') }}
account.{{ account_no }}.dtmf.type = {{ line['XX_dtmf_type']|d('2') }}
handset.{{ account_no }}.name = {{ line['display_name'] }}
voice_mail.number.{{ account_no }} = {{ line['voicemail']|d('%NULL%') }}
{% else -%}
account.{{ account_no }}.enable = 0
account.{{ account_no }}.display_name = %NULL%
account.{{ account_no }}.auth_name = %NULL%
account.{{ account_no }}.user_name = %NULL%
account.{{ account_no }}.password = %NULL%
account.{{ account_no }}.sip_server.1.address = %NULL%
account.{{ account_no }}.sip_server.1.port = %NULL%
account.{{ account_no }}.sip_server.2.address = %NULL%
account.{{ account_no }}.sip_server.2.port = %NULL%
account.{{ account_no }}.dtmf.type = 2
handset.{{ account_no }}.name = %NULL%
voice_mail.number.{{ account_no }} = %NULL%
{% endif %}
{% endfor %}


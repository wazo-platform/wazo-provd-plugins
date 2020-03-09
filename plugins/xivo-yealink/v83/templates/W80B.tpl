#!version:1.0.0.1

static.auto_provision.pnp_enable = 0
static.auto_provision.custom.protect = 1
static.auto_provision.handset_configured.enable = 1

custom.handset.date_format = 2
custom.handset.screen_saver.enable = 0

sip.notify_reboot_enable = 0

{% if vlan_enabled -%}
static.network.vlan.internet_port_enable = 1
static.network.vlan.internet_port_vid = {{ vlan_id }}
static.network.vlan.internet_port_priority = {{ vlan_priority|d('%NULL%') }}
{% else -%}
static.network.vlan.internet_port_enable = 0
static.network.vlan.internet_port_vid = %NULL%
static.network.vlan.internet_port_priority = %NULL%
{% endif %}

{% if syslog_enabled -%}
static.syslog.mode = 1
static.syslog.server = {{ syslog_ip }}
{% else -%}
static.syslog.mode = 0
static.syslog.server = %NULL%
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

{% if XX_xivo_phonebook_url -%}
remote_phonebook.data.1.url = {{ XX_xivo_phonebook_url }}
remote_phonebook.data.1.name = Wazo
{% else -%}
remote_phonebook.data.1.url = %NULL%
remote_phonebook.data.1.name = %NULL%
{% endif %}

static.security.user_name.user = {{ user_username|d('user') }}
static.security.user_name.admin = {{ admin_username|d('admin') }}
static.security.user_password = {{ user_username|d('user') }}:{{ user_password|d('user') }}
static.security.user_password = {{ admin_username|d('admin') }}:{{ admin_password|d('admin') }}

{% for line_no, line in XX_sip_lines.iteritems() -%}
{% if line -%}
account.{{ line_no }}.enable = 1
account.{{ line_no }}.label = {{ line['number']|d(line['display_name']) }}
account.{{ line_no }}.display_name = {{ line['display_name'] }}
account.{{ line_no }}.auth_name = {{ line['auth_username'] }}
account.{{ line_no }}.user_name = {{ line['username'] }}
account.{{ line_no }}.password = {{ line['password'] }}
account.{{ line_no }}.sip_server.1.address = {{ line['proxy_ip'] }}
account.{{ line_no }}.sip_server.1.port = {{ line['proxy_port']|d('%NULL%') }}
account.{{ line_no }}.sip_server.2.address = {{ line['backup_proxy_ip']|d('%NULL%') }}
account.{{ line_no }}.sip_server.2.port = {{ line['backup_proxy_port']|d('%NULL%') }}
account.{{ line_no }}.fallback.redundancy_type = 1
account.{{ line_no }}.cid_source = 2
account.{{ line_no }}.alert_info_url_enable = 0
account.{{ line_no }}.nat.udp_update_enable = 1
account.{{ line_no }}.dtmf.type = {{ line['XX_dtmf_type']|d('2') }}
account.{{ line_no }}.dtmf.info_type = 1
voice_mail.number.{{ line_no }} = {{ line['voicemail']|d('%NULL%') }}
{% else -%}
account.{{ line_no }}.enable = 0
account.{{ line_no }}.label = %NULL%
account.{{ line_no }}.display_name = %NULL%
account.{{ line_no }}.auth_name = %NULL%
account.{{ line_no }}.user_name = %NULL%
account.{{ line_no }}.password = %NULL%
account.{{ line_no }}.sip_server.1.address = %NULL%
account.{{ line_no }}.sip_server.1.port = %NULL%
account.{{ line_no }}.sip_server.2.address = %NULL%
account.{{ line_no }}.sip_server.2.port = %NULL%
voice_mail.number.{{ line_no }} = %NULL%
{% endif %}
{% endfor %}

{% if XX_options['switchboard'] -%}
call_waiting.enable = 0
{% else -%}
call_waiting.enable = 1
{% endif %}

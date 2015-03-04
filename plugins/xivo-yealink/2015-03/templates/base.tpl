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

{% if vlan_enabled and vlan_pc_port_id -%}
network.vlan.pc_port_enable = 1
network.vlan.pc_port_vid = {{ vlan_pc_port_id }}
{% else -%}
network.vlan.pc_port_enable = 0
network.vlan.pc_port_vid = %NULL%
{% endif %}

{% if syslog_enabled -%}
syslog.mode = 1
syslog.server = {{ syslog_ip }}
{% else -%}
syslog.mode = 0
syslog.server = %NULL%
{% endif %}

lang.wui = {{ XX_lang|d('%NULL%') }}
lang.gui = {{ XX_lang|d('%NULL%') }}

voice.tone.country = {{ XX_country|d('%NULL%') }}

local_time.ntp_server1 = {{ ntp_ip|d('pool.ntp.org') }}
{% if XX_timezone -%}
{{ XX_timezone }}
{% else -%}
local_time.time_zone = %NULL%
local_time.time_zone_name = %NULL%
local_time.summer_time = %NULL%
{% endif %}

local_time.date_format = 2

{% if X_xivo_phonebook_ip -%}
remote_phonebook.data.1.url = http://{{ X_xivo_phonebook_ip }}/service/ipbx/web_services.php/phonebook/search/?name=#SEARCH
remote_phonebook.data.1.name = XiVO
{% else -%}
remote_phonebook.data.1.url = %NULL%
remote_phonebook.data.1.name = %NULL%
{% endif %}

security.user_name.user = {{ user_username|d('user') }}
security.user_name.admin = {{ admin_username|d('admin') }}
security.user_password = {{ user_username|d('user') }}:{{ user_password|d('user') }}
security.user_password = {{ admin_username|d('admin') }}:{{ admin_password|d('admin') }}

{% for line in sip_lines.itervalues() %}

account.{{ line['XX_line_no'] }}.enable = 1
{% block sip_line_label scoped %}
account.{{ line['XX_line_no'] }}.label = {{ line['number']|d(line['display_name']) }}
{% endblock %}
account.{{ line['XX_line_no'] }}.display_name = {{ line['display_name'] }}
account.{{ line['XX_line_no'] }}.auth_name = {{ line['auth_username'] }}
account.{{ line['XX_line_no'] }}.user_name = {{ line['username'] }}
account.{{ line['XX_line_no'] }}.password = {{ line['password'] }}
{% block sip_servers scoped %}
account.{{ line['XX_line_no'] }}.sip_server_host = {{ line['proxy_ip'] }}
account.{{ line['XX_line_no'] }}.sip_server_port = {{ line['proxy_port'] }}
{% endblock %}
account.{{ line['XX_line_no'] }}.cid_source = 2
account.{{ line['XX_line_no'] }}.alert_info_url_enable = 0

account.{{ line['XX_line_no'] }}.dtmf.type = {{ line['XX_dtmf_type']|d('2') }}
account.{{ line['XX_line_no'] }}.dtmf.info_type = 1

voice_mail.number.{{ line['XX_line_no'] }} = {{ line['voicemail']|d('%NULL%') }}

{% endfor -%}

{% if XX_options['switchboard'] -%}
push_xml.sip_notify = 1
call_waiting.enable = 0
{% else -%}
push_xml.sip_notify = 0
call_waiting.enable = 1
{% endif %}

distinctive_ring_tones.alert_info.1.text = ring1
distinctive_ring_tones.alert_info.2.text = ring2
distinctive_ring_tones.alert_info.3.text = ring3
distinctive_ring_tones.alert_info.4.text = ring4
distinctive_ring_tones.alert_info.5.text = ring5
distinctive_ring_tones.alert_info.6.text = ring6
distinctive_ring_tones.alert_info.7.text = ring7
distinctive_ring_tones.alert_info.8.text = ring8

distinctive_ring_tones.alert_info.1.ringer = 1
distinctive_ring_tones.alert_info.2.ringer = 2
distinctive_ring_tones.alert_info.3.ringer = 3
distinctive_ring_tones.alert_info.4.ringer = 4
distinctive_ring_tones.alert_info.5.ringer = 5
distinctive_ring_tones.alert_info.6.ringer = 6
distinctive_ring_tones.alert_info.7.ringer = 7
distinctive_ring_tones.alert_info.8.ringer = 8

directory_setting.url = http://{{ ip }}:{{ http_port }}/directory_setting.xml

{{ XX_fkeys }}


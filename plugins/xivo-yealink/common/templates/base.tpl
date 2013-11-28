#!version:1.0.0.1
## the file header "#!version:..." can not be edited or deleted

{% if vlan_enabled -%}
network.vlan.internet_port_enable = 1
network.vlan.internet_port_vid = {{ vlan_id }}
{% if vlan_priority -%}
network.vlan.internet_port_priority = {{ vlan_priority }}
{% endif -%}
{% if vlan_pc_port_id -%}
network.vlan.pc_port_enable = 1
network.vlan.pc_port_vid = {{ vlan_pc_port_id }}
{% endif -%}
{% endif -%}

{% if syslog_enabled -%}
syslog.server = {{ syslog_ip }}
{% endif -%}

{% if XX_lang -%}
lang.wui = {{ XX_lang }}
lang.gui = {{ XX_lang }}
{% endif -%}

{% if ntp_enabled -%}
local_time.ntp_server1 = {{ ntp_ip }}
{% endif -%}
{{ XX_timezone }}

{% if XX_country -%}
voice.tone.country = {{ XX_country }}
{% endif -%}

{% if X_xivo_phonebook_ip -%}
remote_phonebook.data.1.url = http://{{ X_xivo_phonebook_ip }}/service/ipbx/web_services.php/phonebook/search/?name=#SEARCH
remote_phonebook.data.1.name = XiVO
{% endif -%}

{% if admin_password -%}
security.user_password = {{ admin_username }}:{{ admin_password }}
{% endif -%}

{% if user_password -%}
security.user_password =  {{ user_username }}:{{ user_password }}
{% endif -%}

{% for line in sip_lines.itervalues() %}

account.{{ line['XX_line_no'] }}.enable = 1
account.{{ line['XX_line_no'] }}.label = {{ line['number']|d(line['display_name']) }}
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

{% if line['XX_dtmf_inband_transfer'] -%}
account.{{ line['XX_line_no'] }}.dtmf.type = {{ line['XX_dtmf_inband_transfer'] }}
account.{{ line['XX_line_no'] }}.dtmf.info_type = 1
{% endif -%}

{% if line['voicemail'] -%}
voice_mail.number.{{ line['XX_line_no'] }} = {{ line['voicemail'] }}
{% endif -%}

{% endfor -%}

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

{{ XX_fkeys }}

{% block suffix %}{% endblock %}

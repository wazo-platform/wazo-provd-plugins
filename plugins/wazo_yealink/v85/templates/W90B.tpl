#!version:1.0.0.1

static.auto_provision.server.url = {{ XX_server_url }}/
static.firmware.url = {{ XX_server_url }}/firmware/{{ XX_fw_filename }}

{% if XX_handsets_fw -%}
{% for handset, fw_file in XX_handsets_fw.items() -%}
over_the_air.url.{{ handset }} = {{ XX_server_url }}/firmware/{{ fw_file }}
{% endfor -%}
over_the_air.handset_tip = 0
{%- endif %}

sip.notify_reboot_enable = 0

transfer.dsskey_deal_type = 1

static.security.user_name.user = {{ user_username|d('user') }}
static.security.user_name.admin = {{ admin_username|d('admin') }}
static.security.user_password = {{ user_username|d('user') }}:{{ user_password|d('user') }}
static.security.user_password = {{ admin_username|d('admin') }}:{{ admin_password|d('admin') }}

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

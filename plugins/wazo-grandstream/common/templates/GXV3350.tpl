<?xml version="1.0" encoding="UTF-8" ?>
<gs_provision version="1">
 <config version="1">
    {% if admin_password -%}
    <P2>{{ admin_password|e }}</P2>
    {% endif -%}
    {% if ntp_enabled -%}
    <P30>{{ ntp_ip }}</P30>
    {% endif -%}
    {% if XX_timezone -%}
    <P64>{{ XX_timezone }}</P64>
    {% endif -%}
    {% if XX_locale -%}
    <P1362>{{ XX_locale }}</P1362>
    {% endif -%}
    {% if exten_pickup_call -%}
    <P1347>{{ exten_pickup_call }}</P1347>
    {% endif -%}
    {% if vlan_enabled -%}
    <P51>{{ vlan_id }}</P51>
    {% endif -%}
    {% if vlan_priority is defined -%}
    <P87>{{ vlan_priority }}</P87>
    {% endif -%}
    {% if dns_enabled -%}
    <P92>{{ XX_dns_1 }}</P92>
    <P93>{{ XX_dns_2 }}</P93>
    <P94>{{ XX_dns_3 }}</P94>
    <P95>{{ XX_dns_4 }}</P95>
    {% endif -%}
    <P298>1</P298>
    <P290>{ [*x]+ }</P290>
    <P81>1</P81>
    {# Auto-upgrade firmware, check every day #}
    <P194>2</P194>
    {# Randomize check #}
    <P8458>1</P8458>
    {# Check firmware update between 23:00 and 01:00 #}
    <P285>23</P285>
    <P8459>1</P8459>
    {# Do not ask the user to update #}
    <P8375>0</P8375>
{# SIP per-line settings -#}
{% for line_no, line in sip_lines.iteritems() %}
  {% if line_no == '1' %}
    <P271>1</P271>
    <P270>{{ line['display_name'] }}</P270>
    <P47>{{ line['registrar_ip'] }}</P47>
    <P2312>{{ line['backup_registrar_ip'] }}</P2312>
    <P35>{{ line['auth_username'] }}</P35>
    <P36>{{ line['auth_username'] }}</P36>
    <P34>{{ line['password'] }}</P34>
    <P3>{{ line['display_name'] }}</P3>
    <P33>{{ exten_voicemail }}</P33>
    <P2301>0</P2301>
    <P2302>0</P2302>
    <P2303>1</P2303>
    <P191>0</P191>
  {% else -%}
    {% set position = line_no|int + 2 %}
    <P{{ position }}01>1</P{{ position }}01>
    <P{{ position }}02>{{ line['registrar_ip'] }}</P{{ position }}02>
    <P{{ position }}04>{{ line['auth_username'] }}</P{{ position }}04>
    <P{{ position }}05>{{ line['auth_username'] }}</P{{ position }}05>
    <P{{ position }}06>{{ line['password'] }}</P{{ position }}06>
    <P{{ position }}07>{{ line['display_name'] }}</P{{ position }}07>
    <P{{ position }}17>{{ line['display_name'] }}</P{{ position }}17>
    <P{{ position }}26>{{ exten_voicemail }}</P{{ position }}26>
    <P{{ position }}20>0</P{{ position }}20>
    <P2{{ position }}01>0</P2{{ position }}01>
    <P2{{ position }}02>0</P2{{ position }}02>
    <P2{{ position }}03>1</P2{{ position }}03>
    <P2{{ position }}12>{{ line['backup_registrar_ip'] }}</P2{{ position }}12>
  {% endif -%}
{% endfor %}
{% if XX_mpk -%}
  {% for code, value in XX_mpk -%}
    <{{ code }}>{{ value }}</{{ code }}>
  {% endfor -%}
{% endif -%}
  </config>
</gs_provision>

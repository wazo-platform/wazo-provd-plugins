<?xml version="1.0" encoding="UTF-8" ?>
<gs_provision version="1">
 <config version="1">
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
    <P298>1</P298>
    <P290>{ [*x]+ }</P290>
    <P81>1</P81>
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
{{ XX_fkeys }}
</config>
</gs_provision>


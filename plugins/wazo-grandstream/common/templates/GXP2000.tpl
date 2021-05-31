    {% if ntp_enabled -%}
    P30={{ ntp_ip }}
    {% endif -%}
    {% if XX_timezone -%}
    P64={{ XX_timezone }}
    {% endif -%}
    {% if XX_locale -%}
    P1362={{ XX_locale }}
    {% endif -%}
    {% if exten_pickup_call -%}
    P1347={{ exten_pickup_call }}
    {% endif -%}
    {% if vlan_enabled -%}
    P51={{ vlan_id }}
    {% endif -%}
    {% if vlan_priority is defined -%}
    P87={{ vlan_priority }}
    {% endif -%}
    P298=1
    P290={ [*x]+ }
    P81=1
{# SIP per-line settings -#}
{% for line_no, line in sip_lines.iteritems() %}
  {% if line_no == '1' %}
    P271=1
    P270={{ line['display_name'] }}
    P47={{ line['registrar_ip'] }}
    P2312={{ line['backup_registrar_ip'] }}
    P35={{ line['auth_username'] }}
    P36={{ line['auth_username'] }}
    P34={{ line['password'] }}
    P3={{ line['display_name'] }}
    P33={{ exten_voicemail }}
    P2301=0
    P2302=0
    P2303=1
    P191=0
  {% else -%}
    {% set position = line_no|int + 2 %}
    P{{ position }}01=1
    P{{ position }}02={{ line['registrar_ip'] }}
    P{{ position }}04={{ line['auth_username'] }}
    P{{ position }}05={{ line['auth_username'] }}
    P{{ position }}06={{ line['password'] }}
    P{{ position }}07={{ line['display_name'] }}
    P{{ position }}17={{ line['display_name'] }}
    P{{ position }}26={{ exten_voicemail }}
    P{{ position }}20=0
    P2{{ position }}01=0
    P2{{ position }}02=0
    P2{{ position }}03=1
    P2{{ position }}12={{ line['backup_registrar_ip'] }}
  {% endif -%}
{% endfor %}
{% if XX_fkeys -%}
{% for code, value in XX_fkeys -%}
<{{ code }}>{{ value }}</{{ code }}>
{% endfor -%}
{% endif -%}

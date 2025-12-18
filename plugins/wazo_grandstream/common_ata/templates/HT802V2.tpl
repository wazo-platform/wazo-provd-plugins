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
{% for line_no, line in sip_lines.items() %}
  {% if line_no == '1' %}
    <P47>{{ line['registrar_ip'] }}</P47>
    <P967>{{ line['backup_registrar_ip'] }}</P967>
    <P35>{{ line['auth_username'] }}</P35>
    <P36>{{ line['auth_username'] }}</P36>
    <P34>{{ line['password'] }}</P34>
    <P3>{{ line['display_name'] }}</P3>
    <P191>0</P191>
    <P854>4</P854>
  {% else -%}
    <P703>{{ line['display_name'] }}</P703>
    <P734>{{ line['password'] }}</P734>
    <P735>{{ line['auth_username'] }}</P735>
    <P736>{{ line['auth_username'] }}</P736>
    <P740>5068</P740>
    <P747>{{ line['registrar_ip'] }}</P747>
    <P987>{{ line['backup_registrar_ip'] }}</P987>
    <P751>0</P751>
    <P864>4</P864>
  {% endif -%}
{% endfor %}
    {# Fax-specific -#}
    {# Caller ID Scheme.
    # <value=0>  Bellcore/Telcordia (default)
    # <value=1>  ETSI-FSK during ringing
    # <value=2>  ETSI-FSK prior to ringing with DTAS
    # <value=3>  ETSI-FSK prior to ringing with LR+DTAS
    # <value=4>  ETSI-FSK prior to ringing with RP
    # <value=5>  ETSI-DTMF during ringing
    # <value=6>  ETSI-DTMF prior to ringing with DTAS
    # <value=7>  ETSI-DTMF prior to ringing with LR+DTAS
    # <value=8>  ETSI-DTMF prior to ringing with RP
    # <value=9>  SIN 227 - BT
    # <value=10> NTT Japan
    # <value=11> DTMF Denmark prior to ringing no DTAS no LR
    # <value=12> DTMF Denmark prior to ringing with LR
    # <value=13> DTMF Sweden/Finalnd prior to ringing with LR
    # <value=14> DTMF Brazil
    # Number: 0 to 14
    # Mandatory -#}
    <P863>0</P863>
    {# SLIC Setting.
    # 0 - USA (BELLCORE 600 ohms), 3 - USA 2(BELCORE 600 ohms + 2.16uF), 11 - AUSTRAILA, 5 - CHINA CO, 6 - CHINA PBX, 4 - EUROPEAN CTR21
    # 9 - GERMANY, 8 -INDIA/NEW ZEALAND, 2 - JAPAN CO, 7 - JAPAN PBX, 1 - STANDARD 900 omhs, 10 - UK
    # Number: 0-11
    # Mandatory -#}
    <P854>4</P854>
    {# FAX Mode. 0 - T.38 (Auto Detect), 1 - Pass Through
    # Number: 0, 1
    # Mandatory -#}
    <P228>0</P228>
    {# Re-INVITE After Fax Tone Detected. 0 - Disabled, 1 - Enabled.
    # Number: 0, 1
    # Mandatory -#}
    <P4417>1</P4417>
    <P20502>1</P20502>
    {# 1 - HTTP server firmware upgrade -#}
    <P6767>1</P6767>
    {# URL firmware upgrade -#}
    <P192>{{ XX_server_url_without_scheme }}/Grandstream/</P192>
  </config>
</gs_provision>

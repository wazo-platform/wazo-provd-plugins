{% macro dst_change(suffix, value) -%}
<DST_{{ suffix }}_Mon>{{ value['month'] }}</DST_{{ suffix }}_Mon>
<DST_{{ suffix }}_Hour>{{ value['hour'] }}</DST_{{ suffix }}_Hour>
<DST_{{ suffix }}_Wday>{{ value['dst_wday'] }}</DST_{{ suffix }}_Wday>
{% if value['dst_week'] -%}
<DST_{{ suffix }}_Week>{{ value['dst_week'] }}</DST_{{ suffix }}_Week>
{% endif -%}
<DST_{{ suffix }}_Min>0</DST_{{ suffix }}_Min>
{% endmacro -%}
<?xml version="1.0" encoding="UTF-8" ?>
<VOIP_CONFIG_FILE>
<version>2.0002</version>

<GLOBAL_CONFIG_MODULE>
{% if ntp_enabled -%}
<SNTP_Server>{{ ntp_ip }}</SNTP_Server>
<Enable_SNTP>1</Enable_SNTP>
<SNTP_Timeout>60</SNTP_Timeout>
{% else -%}
<Enable_SNTP>0</Enable_SNTP>
{% endif -%}
<Language>{{ XX_locale }}</Language>
{% if XX_timezone -%}
<Time_Zone>{{ XX_timezone['time_zone'] }}</Time_Zone>
<Time_Zone_Name>{{ XX_timezone['time_zone_name'] }}</Time_Zone_Name>
{% if not XX_timezone['enable_dst'] -%}
<Enable_DST>0</Enable_DST>
{% else -%}
<Enable_DST>2</Enable_DST>
<DST_Min_Offset>{{ XX_timezone['dst_min_offset'] }}</DST_Min_Offset>
{{ dst_change('Start', XX_timezone['dst_start']) }}
{{ dst_change('End', XX_timezone['dst_end']) }}
{% endif -%}
{% endif -%}
</GLOBAL_CONFIG_MODULE>

<MMI_CONFIG_MODULE>
<Web_Port>80</Web_Port>
<Web_Server_Type>0</Web_Server_Type>
<Https_Web_Port>443</Https_Web_Port>
<Enable_MMI_Filter>0</Enable_MMI_Filter>
<Web_Authentication>0</Web_Authentication>
<Default_WEB_User>0</Default_WEB_User>
<MMI_Account>
{% if admin_password -%}
<MMI_Account_Entry>
<ID>Account1</ID>
<Name>admin</Name>
<Password>{{ admin_password }}</Password>
<Level>10</Level>
</MMI_Account_Entry>
{% endif -%}
{% if user_password -%}
<MMI_Account_Entry>
<ID>Account2</ID>
<Name>guest</Name>
<Password>{{ user_password }}</Password>
<Level>5</Level>
</MMI_Account_Entry>
{% endif -%}
</MMI_Account>
</MMI_CONFIG_MODULE>

<SIP_CONFIG_MODULE>
<SIP__Port>5060</SIP__Port>
<SIP_Line_List>
{% for line_no, line in sip_lines.iteritems() -%}
{% if line -%}
<SIP_Line_List_Entry>
<ID>SIP{{ line_no }}</ID>
<Phone_Number>{{ line['username']}}</Phone_Number>
<Display_Name>{{ line['number'] }} {{ line['display_name']|e }}</Display_Name>
<Register_Addr>{{ line['proxy_ip'] }}</Register_Addr>
<Register_Port>{{ line['proxy_port']|d(5060) }}</Register_Port>
<Register_User>{{ line['username'] }}</Register_User>
<Register_Pswd>{{ line['password'] }}</Register_Pswd>
<Register_TTL>60</Register_TTL>
<Enable_Reg>1</Enable_Reg>
<Transport>{{ X_sip_transport_protocol }}</Transport>
<DTMF_Mode>{{ line['XX_dtmf_mode'] }}</DTMF_Mode>
{% if line['voicemail'] -%}
<MWI_Num>{{ line['voicemail'] }}</MWI_Num>
{% else -%}
<MWI_Num></MWI_Num>
{% endif -%}
</SIP_Line_List_Entry>
{% else -%}
<SIP_Line_List_Entry>
<ID>SIP{{ line_no }}</ID>
<Phone_Number></Phone_Number>
<Display_Name></Display_Name>
<Register_Addr></Register_Addr>
<Register_Port></Register_Port>
<Register_User></Register_User>
<Register_Pswd></Register_Pswd>
<Enable_Reg>0</Enable_Reg>
</SIP_Line_List_Entry>
{% endif %}
{% endfor %}
</SIP_Line_List>
</SIP_CONFIG_MODULE>

<QOS_CONFIG_MODULE>
{% if vlan_enabled -%}
<Enable_VLAN>1</Enable_VLAN>
<VLAN_ID>{{ vlan_id }}</VLAN_ID>
<Signalling_Priority>{{ vlan_priority|d('%NULL%') }}</Signalling_Priority>
<Voice_Priority>{{ vlan_priority|d('%NULL%') }}</Voice_Priority>
{% else -%}
<Enable_VLAN>0</Enable_VLAN>
<VLAN_ID>256</VLAN_ID>
<Signalling_Priority>0</Signalling_Priority>
<Voice_Priority>0</Voice_Priority>
{% endif %}
</QOS_CONFIG_MODULE>

{% if syslog_enabled -%}
<AAA_CONFIG_MODULE>
<Enable_Syslog>1</Enable_Syslog>
<Syslog_address>{{ syslog_ip }}</Syslog_address>
<Syslog_port>{{ syslog_port }}</Syslog_port>
</AAA_CONFIG_MODULE>
{% else -%}
<AAA_CONFIG_MODULE>
<Enable_Syslog>0</Enable_Syslog>
<Syslog_address>0.0.0.0</Syslog_address>
<Syslog_port>514</Syslog_port>
</AAA_CONFIG_MODULE>
{% endif -%}

<PHONE_CONFIG_MODULE>
{% if admin_password -%}
<Menu_Password>{{ admin_password }}</Menu_Password>
{% else -%}
<Menu_Password>123</Menu_Password>
{% endif -%}
{% for line_no, line in sip_lines.iteritems() %}
<LCD_Title>{{ line['display_name']|e }} {{ line['number'] }}</LCD_Title>
{% endfor %}
<Time_Display_Style>0</Time_Display_Style>
<Date_Display_Style>2</Date_Display_Style>

<Function_Key>
{% for fkey in XX_fkeys -%}
<Function_Key_Entry>
<ID>Fkey{{ fkey['id'] }}</ID>
<Type>1</Type>
<Value>{{ fkey['value'] }}</Value>
<Title>{{ fkey['title'] }}</Title>
</Function_Key_Entry>
{% endfor -%}
</Function_Key>
</PHONE_CONFIG_MODULE>
</VOIP_CONFIG_FILE>

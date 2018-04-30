<?xml version="1.0" encoding="UTF-8" ?>
<VOIP_CONFIG_FILE>
<version>2.0002</version>

<GLOBAL_CONFIG_MODULE>
<SNTP_Server>{{ ntp_ip }}</SNTP_Server>
<Enable_SNTP>1</Enable_SNTP>
<Time_Zone>4</Time_Zone>
<Location>10</Location>
<Time_Zone_Name>UTC+1</Time_Zone_Name>
<Language>4</Language>
<Enable_DST>1</Enable_DST>
<DST_Fixed_Type>2</DST_Fixed_Type>
<SNTP_Timeout>60</SNTP_Timeout>
<DST_Min_Offset>60</DST_Min_Offset>
<DST_Start_Mon>3</DST_Start_Mon>
<DST_Start_Week>-1</DST_Start_Week>
<DST_Start_Wday>1</DST_Start_Wday>
<DST_Start_Hour>1</DST_Start_Hour>
<DST_End_Mon>10</DST_End_Mon>
<DST_End_Week>-1</DST_End_Week>
<DST_End_Wday>1</DST_End_Wday>
<DST_End_Hour>1</DST_End_Hour>
</GLOBAL_CONFIG_MODULE>

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
<DTMF_Mode>2</DTMF_Mode>
<MWI_Num>*98</MWI_Num>
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

<PHONE_CONFIG_MODULE>
{% for line_no, line in sip_lines.iteritems() %}
<LCD_Title>{{ line['display_name']|e }} {{ line['number'] }}</LCD_Title>
{% endfor %}
<Time_Display_Style>0</Time_Display_Style>
<Date_Display_Style>2</Date_Display_Style>

<Function_Key>
{{ XX_fkeys }}
</Function_Key>
</PHONE_CONFIG_MODULE>
</VOIP_CONFIG_FILE>

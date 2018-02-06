<?xml version="1.0" encoding="UTF-8" ?>
<VOIP_CONFIG_FILE>
<version>2.0002</version>
<GLOBAL_CONFIG_MODULE>
<SNTP_Server>{{ ntp_ip }}</SNTP_Server>
<Enable_SNTP>1</Enable_SNTP>
{{ XX_timezone }}
</GLOBAL_CONFIG_MODULE>
<SIP_CONFIG_MODULE>
<SIP__Port>5060</SIP__Port>
<SIP_Line_List>
<SIP_Line_List_Entry>
<ID>SIP1</ID>
{% for line_no, line in sip_lines.iteritems() %}
<Phone_Number>{{ line['username']}}</Phone_Number>
<Display_Name>{{ line['display_name']|e }}</Display_Name>
<Register_Addr>{{ line['proxy_ip'] }}</Register_Addr>
<Register_Port>{{ line['proxy_port']|d(5060) }}</Register_Port>
<Register_User>{{ line['username'] }}</Register_User>
<Register_Pswd>{{ line['password'] }}</Register_Pswd>
<Register_TTL>60</Register_TTL>
<Enable_Reg>1</Enable_Reg>
<Proxy_Addr>{{ line['proxy_ip'] }}</Proxy_Addr>
<Proxy_Port>{{ line['proxy_port']|d(5060) }}</Proxy_Port>
<Proxy_User>{{ line['username'] }}</Proxy_User>
<Proxy_Pswd>{{ line['password'] }}</Proxy_Pswd>
{% if line['backup_proxy_ip'] -%}
<BakProxy_Addr>{{ line['backup_proxy_ip'] }}</BakProxy_Addr>
<BakProxy_Port>{{ line['backup_proxy_port']|d(5060) }}</BakProxy_Port>
{% endif %}
{% endfor %}
<DTMF_Mode>2</DTMF_Mode>
<MWI_Num>*98</MWI_Num>
</SIP_Line_List_Entry>
</SIP_Line_List>
</SIP_CONFIG_MODULE>
<PHONE_CONFIG_MODULE>
{% for line_no, line in sip_lines.iteritems() %}
<LCD_Title>{{ line['display_name']|e }} {{ line['number'] }}</LCD_Title>
{% endfor %}
<Function_Key>
<function_key_entry>
<id>fkey1</id>
<type>2</type>
<value>sip1</value>
<title></title>
</function_key_entry>
<function_key_entry>
<id>fkey2</id>
<type>2</type>
<value>sip0</value>
<title></title>
</function_key_entry>
<function_key_entry>
<id>fkey3</id>
<type>2</type>
<value>sip0</value>
<title></title>
</function_key_entry>
<function_key_entry>
<id>fkey4</id>
<type>2</type>
<value>sip0</value>
<title></title>
</function_key_entry>
<Function_Key_Entry>
<ID>Fkey5</ID>
<Type>3</Type>
<Value>F_RELEASE</Value>
<Title></Title>
</Function_Key_Entry>
<Function_Key_Entry>
<ID>Fkey6</ID>
<Type>1</Type>
<Value>*98@1/m</Value>
<Title></Title>
</Function_Key_Entry>
<Function_Key_Entry>
<ID>Fkey7</ID>
<Type>3</Type>
<Value>F_HEADSET</Value>
<Title></Title>
</Function_Key_Entry>
{{ XX_fkeys }}
</PHONE_CONFIG_MODULE>
</VOIP_CONFIG_FILE>

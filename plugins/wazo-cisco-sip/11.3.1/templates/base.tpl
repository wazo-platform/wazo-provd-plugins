<?xml version="1.0" standalone="yes"?>
<flat-profile>

<!--  System Configuration  -->
<Restricted_Access_Domains ua="na"/>
<Enable_Web_Server ua="na">Yes</Enable_Web_Server>
<Enable_Protocol ua="na">Http</Enable_Protocol>

<Phone-UI-readonly ua="na">No</Phone-UI-readonly>
<Phone-UI-User-Mode ua="na">Yes</Phone-UI-User-Mode>

#<!--  Network Settings  -->
<IP_Mode ua="na"/>

#<Device_Administration ua="na">No</Device_Administration>

#<!-- Network Configuration -->
#<Network_Configuration ua="na">IPv4 Only</Network_Configuration>

<!-- Network Configuration -->
<Network_Configuration ua="na"/>

<!--  IPv4 Settings   -->
<Connection_Type ua="na">DHCP</Connection_Type>
<!--  available options: DHCP|Static IP  -->
<Static_IP ua="na"/>
<NetMask ua="na"/>
<Gateway ua="na"/>
<Primary_DNS ua="na"/>
<Secondary_DNS ua="na"/>

<!--  IPv6 Settings   -->
<IPv6_Connection_Type ua="na">DHCP</IPv6_Connection_Type>
<!--  available options: DHCP|Static IP  -->
<IPv6_Static_IP ua="na"/>
<Prefix_Length ua="na">1</Prefix_Length>
<IPv6_Gateway ua="na"/>
<IPv6_Primary_DNS ua="na"/>
<IPv6_Secondary_DNS ua="na"/>
<Broadcast_Echo ua="na">Disabled</Broadcast_Echo>
<Auto_Config ua="na">Enabled</Auto_Config>
<!--  available options: Disabled|Enabled  -->

<!--  802.1X Authentication  -->
<Enable_802.1X_Authentication ua="na">No</Enable_802.1X_Authentication>

<!--  Optional Network Configuration  -->
<Host_Name ua="na"/>
<Domain ua="na"/>

<Primary_NTP_Server ua="na"/>
<Secondary_NTP_Server ua="na"/>

<!--  Screen  -->
<Screen_Saver_Enable ua="rw">Yes</Screen_Saver_Enable>
<Screen_Saver_Type ua="rw">Clock</Screen_Saver_Type>
<!--  available options: Clock|Download Picture|Logo  -->
<Screen_Saver_Wait ua="rw">300</Screen_Saver_Wait>
<Screen_Saver_Refresh_Period ua="rw">10</Screen_Saver_Refresh_Period>
<Back_Light_Timer ua="rw">5m</Back_Light_Timer>
<!--  available options: 1m|5m|30m|Always On  -->

<!--  Password for Factory Reset  -->
<Protect_IVR_FactoryReset ua="na">Yes</Protect_IVR_FactoryReset>

<!--  VLAN Settings  -->
<Enable_VLAN ua="na">No</Enable_VLAN>
<VLAN_ID ua="na">1</VLAN_ID>

{% if admin_password is defined -%}
<Admin_Password>{{ admin_password|e }}</Admin_Password>
{% endif -%}

<User_Password></User_Password>

{% if dns_enabled -%}
<Primary_DNS>{{ dns_ip }}</Primary_DNS>
{% endif -%}

{% if ntp_enabled -%}
<Primary_NTP_Server>{{ ntp_ip }}</Primary_NTP_Server>
{% endif -%}

{% if syslog_enabled -%}
<Syslog_Server>{{ syslog_ip }}:{{ syslog_port }}</Syslog_Server>
{% endif -%}

{% if vlan_enabled -%}
<Enable_VLAN>Yes</Enable_VLAN>
<VLAN_ID>{{ vlan_id }}</VLAN_ID>
{% if vlan_pc_port_id is defined -%}
<Enable_PC_Port_VLAN_Tagging>Yes</Enable_PC_Port_VLAN_Tagging>
<PC_Port_VLAN_ID>{{ vlan_pc_port_id }}</PC_Port_VLAN_ID>
{% endif -%}
{% endif -%}

{% block upgrade_rule -%}
<Upgrade_Rule></Upgrade_Rule>
{% endblock -%}

{% if exten_voicemail is defined -%}
<Voice_Mail_Number>{{ exten_voicemail }}</Voice_Mail_Number>
{% endif -%}
{% if exten_pickup_call is defined -%}
<Call_Pickup_Code>{{ exten_pickup_call }}</Call_Pickup_Code>
{% endif -%}
{% if exten_pickup_group is defined -%}
<Group_Call_Pickup_Code>{{ exten_pickup_group }}</Group_Call_Pickup_Code>
{% endif -%}


{% if '1' in sip_lines -%}
<Station_Name>{{ sip_lines['1']['display_name']|e }}</Station_Name>
{% endif -%}

{% block dictionary_server_script -%}
<Dictionary_Server_Script></Dictionary_Server_Script>
{% endblock -%}
<Language_Selection>{{ XX_language }}</Language_Selection>
<Locale>{{ XX_locale }}</Locale>
{{ XX_timezone }}

{% for line_no, line in sip_lines.iteritems() %}
<Line_Enable_{{ line_no }}_>Yes</Line_Enable_{{ line_no }}_>
<Proxy_{{ line_no }}_>{{ XX_proxies[line_no] }}</Proxy_{{ line_no }}_>
<Use_DNS_SRV_{{ line_no }}_>Yes</Use_DNS_SRV_{{ line_no }}_>
<Proxy_Fallback_Intvl_{{ line_no }}_>120</Proxy_Fallback_Intvl_{{ line_no }}_>
<Display_Name_{{ line_no }}_>{{ line['display_name']|e }}</Display_Name_{{ line_no }}_>
<User_ID_{{ line_no }}_>{{ line['username']|e }}</User_ID_{{ line_no }}_>
<Password_{{ line_no }}_>{{ line['password']|e }}</Password_{{ line_no }}_>
<Auth_ID_{{ line_no }}_>{{ line['auth_username']|e }}</Auth_ID_{{ line_no }}_>
{% set dtmf_mode = line['dtmf_mode'] or sip_dtmf_mode -%}
{% if dtmf_mode == 'RTP-in-band' -%}
<DTMF_Tx_Method_{{ line_no }}_>InBand</DTMF_Tx_Method_{{ line_no }}_>
{% elif dtmf_mode == 'RTP-out-of-band' -%}
<DTMF_Tx_Method_{{ line_no }}_>AVT</DTMF_Tx_Method_{{ line_no }}_>
{% elif dtmf_mode == 'SIP-INFO' -%}
<DTMF_Tx_Method_{{ line_no }}_>INFO</DTMF_Tx_Method_{{ line_no }}_>
{% else -%}
<DTMF_Tx_Method_{{ line_no }}_>Auto</DTMF_Tx_Method_{{ line_no }}_>
{% endif -%}
{% endfor -%}

{% block suffix %}{% endblock %}

<!-- Function keys definition SHOULD go before the line key definition if we
     want the line key definition to override the function key definition -->
{{ XX_fkeys }}

{% for line_no, line in sip_lines.iteritems() %}
<Extension_{{ line_no }}_>{{ line_no }}</Extension_{{ line_no }}_>
<Short_Name_{{ line_no }}_>{{ line['number']|d('$USER') }}</Short_Name_{{ line_no }}_>
<Extended_Function_{{ line_no }}_></Extended_Function_{{ line_no }}_>
{% endfor %}

{% if XX_xivo_phonebook_url -%}
<XML_Directory_Service_Name>{{ XX_directory_name }}</XML_Directory_Service_Name>
<XML_Directory_Service_URL>{{ XX_xivo_phonebook_url|e }}</XML_Directory_Service_URL>
{% endif -%}
</flat-profile>

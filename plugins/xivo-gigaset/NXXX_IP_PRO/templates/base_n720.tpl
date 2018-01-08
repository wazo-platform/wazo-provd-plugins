<?xml version="1.0" encoding="ISO-8859-1"?>
<ProviderFrame xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="N510.xsd">
  <Provider>
<!-- Please enter the correct MAC Address example: 3E2F800E1234
	 Please enter a Profile name 
	 If not correct, no setting will be done
-->
    <MAC_ADDRESS value="7C2F80FFFFFF"/>
    <PROFILE_NAME class="string" value="N720"/>	

<!-- Allow access from other networks. -->
    <SYMB_ITEM ID="BS_IP_Data1.ucB_ACCEPT_FOREIGN_SUBNET" class="symb_item" value="0x1"/>
    
<!-- WEB-UI: Settings - Telephony - Connections - Connection Name or Number -->
    <SYMB_ITEM ID="BS_Accounts.astAccounts[0].aucAccountName[0]" class="symb_item" value='"{{ line['display_name'] }}"'/>
    
{% for line_no, line in sip_lines.iteritems() %}
    <SYMB_ITEM ID="BS_IP_Data1.aucS_SIP_ACCOUNT_NAME_{{ line_no }}" class="symb_item" value='"{{ line['display_name'] }}"'/>
    <SYMB_ITEM ID="BS_IP_Data1.aucS_SIP_DISPLAYNAME_{{ line_no }}" class="symb_item" value='"{{ line['display_name'] }}"'/>
    <SYMB_ITEM ID="BS_IP_Data3.aucS_SIP_LOGIN_ID_{{ line_no }}" class="symb_item" value='"{{ line['username'] }}"'/>
    <SYMB_ITEM ID="BS_IP_Data1.aucS_SIP_PASSWORD_{{ line_no }}" class="symb_item" value='"{{ line['password'] }}"'/>
    <SYMB_ITEM ID="BS_IP_Data1.aucS_SIP_USER_ID_{{ line_no }}" class="symb_item" value='"{{ line['auth_username'] }}"'/>
    <SYMB_ITEM ID="BS_IP_Data1.aucS_SIP_DOMAIN_{{ line_no }}" class="symb_item" value='"{{ line['proxy_ip'] }}"'/>
    <SYMB_ITEM ID="BS_IP_Data1.aucS_SIP_SERVER_{{ line_no }}" class="symb_item" value='"{{ line['proxy_ip'] }}"' />
    <SYMB_ITEM ID="BS_IP_Data1.aucS_SIP_REGISTRAR_{{ line_no }}" class="symb_item" value='"{{ line['proxy_ip'] }}"'/>
    <SYMB_ITEM ID="BS_IP_Data1.aucS_STUN_SERVER_{{ line_no }}" class="symb_item" value='""'/>
    <SYMB_ITEM ID="BS_IP_Data1.aucS_OUTBOUND_PROXY_{{ line_no }}" class="symb_item" value='""'/>
    <SYMB_ITEM ID="BS_IP_Data1.aucS_SIP_PROVIDER_NAME_{{ line_no }}" class="symb_item" value='"{{ line['display_name'] }}"'/>
    <SYMB_ITEM ID="BS_IP_Data1.uiI_SIP_SERVER_PORT_{{ line_no }}" class="symb_item" value="0x13c4"/>
    <SYMB_ITEM ID="BS_IP_Data1.uiI_SIP_REGISTRAR_PORT_{{ line_no }}" class="symb_item" value="0x13c4"/>
    <SYMB_ITEM ID="BS_IP_Data1.ucB_SIP_USE_STUN_{{ line_no }}" class="symb_item" value="0x0"/>
    <SYMB_ITEM ID="BS_IP_Data1.uiI_STUN_SERVER_PORT_{{ line_no }}" class="symb_item" value="0xd96"/>
    <SYMB_ITEM ID="BS_IP_Data1.ucI_OUTBOUND_PROXY_MODE_{{ line_no }}" class="symb_item" value="0x1"/>
    <SYMB_ITEM ID="BS_IP_Data1.uiI_OUTBOUND_PROXY_PORT_{{ line_no }}" class="symb_item" value="0x13c4"/>
    <SYMB_ITEM ID="BS_IP_Data1.uiI_RE_REGISTRATION_TIMER_{{ line_no }}" class="symb_item" value="0xb4"/>
    <SYMB_ITEM ID="BS_IP_Data1.uiI_RE_STUN_TIMER_{{ line_no }}" class="symb_item" value="0xf0"/>
{% endfor -%}

<!-- Auto Provisioning - Selected Codec settings 0x00(G.711ulaw),0x01(G.711alaw),0x02(G.726),0x03(G.729),0x05(G722) -->
    <SYMB_ITEM ID="BS_IP_Data1.ucI_CODEC_PREFERENCES" class="symb_item" value="0"/>
    <SYMB_ITEM ID="BS_IP_Data1.ucI_SIP_PREFERRED_VOCODER" class="symb_item" value="0x05,0x01,0x00,0x02,0x03"/>   

<!-- WEB UI: Settings - Telephony - Connections - Active
     Enable the SIP account -->
    <SYMB_ITEM ID="BS_IP_Data1.ucB_SIP_ACCOUNT_IS_ACTIVE_1" class="symb_item" value="0x1"/>  

<!-- VoIP Account 2 example, Account 3-6 can be added copy account 2 data and increase the account number -->

<!-- WEB-UI: Settings - Telephony - Connections - Connection Name or Number -->
    <SYMB_ITEM ID="BS_Accounts.astAccounts[1].aucAccountName[0]" class="symb_item" value='"1023"'/>
    

<!-- Auto Provisioning - Selected Codec settings 0x00(G.711ulaw),0x01(G.711alaw),0x02(G.726),0x03(G.729),0x05(G722) -->
    <SYMB_ITEM ID="BS_IP_Data1.ucI_SIP_PREFERRED_VOCODER_2" class="symb_item" value="0x05,0x01,0x00,0x02,0x03"/> 

<!-- WEB UI: Settings - Telephony - Connections - Active
     Enable the SIP account -->
    <SYMB_ITEM ID="BS_IP_Data1.ucB_SIP_ACCOUNT_IS_ACTIVE_2" class="symb_item" value="0x1"/> 
    
<!-- Autoprovisioning - Account - Label? Change the name of handset 1 -->	
    <SYMB_ITEM ID="BS_AE_Subscriber.stMtDat[0].aucTlnName[0]" class="symb_item" value='"Handset1"'/>
    <!-- Example to change the name of Handset 2 	
    <SYMB_ITEM ID="BS_AE_Subscriber.stMtDat[1].aucTlnName[0]" class="symb_item" value='"Handset2"'/> -->
        
<!-- Change DTMF to RFC2833 compatible with RFC4733 -->    
    <SYMB_ITEM ID="BS_IP_Data1.ucB_DTMF_TX_MODE_AUTO" class="symb_item" value="0"/>
    <SYMB_ITEM ID="BS_IP_Data1.ucI_DTMF_TX_MODE_BITS" class="symb_item" value="2"/>
    
	
<!-- Change the Voicemail number to *2 -->	
    <SYMB_ITEM ID="BS_IP_Data1.aucS_VOIP_NET_AM_NUMBER_1" class="symb_item" value='"*2"'/>
    <SYMB_ITEM ID="BS_IP_Data1.aucS_VOIP_NET_AM_NUMBER_2" class="symb_item" value='"*2"'/>
    
<!-- Autoprovisioning - Features - Voicemail -->    
    <SYMB_ITEM ID="BS_IP_Data1.ucB_VOIP_NET_AM_ENABLED_1" class="symb_item" value="0x1"/>
    <SYMB_ITEM ID="BS_IP_Data1.ucB_VOIP_NET_AM_ENABLED_2" class="symb_item" value="0x1"/>

<!-- Needed to enable Provisioning, After Reboot -->	
    <SYMB_ITEM ID="BS_IP_Data.ucB_AUTO_UPDATE_PROFILE" class="symb_item" value="0x1"/>
    <SYMB_ITEM ID="BS_IP_Data3.ucI_ONESHOT_PROVISIONING_MODE_1" class="symb_item" value="0x1"/>
    
<!-- Enable Session timer minimum value is 90 seconds -->    
    <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].ulSessionRefresh_MIN_SE" class="symb_item" value="90"/>
    
<!-- Increase lenght handset name on display -->    
    <SYMB_ITEM ID="BS_LM_AppCfg.bit.bHasIdleTextInternalName" class="symb_item" value="1"/>

<!-- WEB UI: Settings - Management - Firmware update - Data Server
     Redirect device always to own provisioning Server so you are in control for example: Firmware updates 	
    <SYMB_ITEM ID="BS_IP_Data1.aucS_DATA_SERVER[0]" class="symb_item" value='"192.168.178.101"'/> -->

<!-- WEB UI: Settings - Telephony - Advanced VoIP Settings - Transfer Call by On Hook
     Call Transfer by ending the call -->	
    <SYMB_ITEM ID="BS_IP_Data1.ucB_CT_AFTER_ON_HOOK" class="symb_item" value="0x1"/>
    <SYMB_ITEM ID="BS_CUSTOM_ORG.bit.bEct" class="symb_item" value="0x1"/>

<!-- WEB UI: Settings - Management - Local Settings - Tone Selection
	 International=0, US=1, CH=2, AUS=4, ES=6, FR=7, UK=8, NL=9, PL=10, Russia=11, DE=12, IT=13 -->
    <SYMB_ITEM ID="BS_AE_SwConfig.ucCountryCodeTone" class="symb_item" value="0"/>
    
<!-- Http language of the device
	 English=0x1,German=0x2,Spanish=0x4,Italian=0x7,French=0x9,Dutch=0xa,Turkish=0x10,Polski=0x11 -->	
    <SYMB_ITEM ID="BS_IP_Data1.ucI_HTTPLANGUAGE" class="symb_item" value="0x1"/> 

<!-- WEB UI: Settings - Management - Date&Time  
	 Time Country: NL=0x30, UK=0x4A, DE=0x19, FR=0x18 --> 	
    <SYMB_ITEM ID="BS_IP_Data1.uiI_TIME_COUNTRY" class="symb_item" value="0x30"/>   

<!-- WEB UI: Settings - Management - Local Settings - Select Country optimum setting for behind other platformen is "Other country"--> 
    <SYMB_ITEM ID="BS_IP_Data1.ucI_DIALING_PLAN_COUNTRY_ID" class="symb_item" value="0xff"/>    
    
<!-- Autoprovisioning - Preference - Admin Password. The default setting for the PIN is 0000 (0x00,0x00). Enter a new 4-digit 
    system PIN for the base station - four digits from 0 to 9. Example: PIN='1234' please enter '0x12,0x34' -->
    <SYMB_ITEM ID="BS_CUSTOM.aucKdsPin[0]" class="symb_item" value="0x00,0x00"/>    
    
<!-- Autoprovisioning - Preference - Time Zone: 
     0x00(GMT-12),0x01(GMT-11),0x02(GMT-10),0x03(GMT-9),0x04(GMT-8),0x07(GMT-7),0x09(GMT-6),0x0d(GMT-5),0x0f(GMT-4),0x15(GMT-3),0x16(GMT-2),
     0x18(GMT-1),0x1a(GMT),0x1b(GMT+1),0x20(GMT+2),0x28(GMT+3),0x2b(GMT+4),0x2e(GMT+5),0x33(GMT+6),0x37(GMT+7),0x3a(GMT+8),0x3d(GMT+9),0x43(GMT+10) -->    
    <SYMB_ITEM ID="BS_IP_Data1.uiI_TIME_TIMEZONE" class="symb_item" value="0x1b"/>  

<!-- Autoprovisioning - Preference - Primary NTP server -->    
    <SYMB_ITEM ID="BS_IP_Data1.aucS_TIME_NTP_SERVER" class="symb_item" value='"cn.pool.ntp.org"'/>
    
<!-- Autoprovisioning - Preference - Daylight Saving time: 0x1(enabled),0x0(Disabled) -->
    <SYMB_ITEM ID="BS_IP_Data1.ucB_TIME_USE_AUTOMATIC_DST" class="symb_item" value="0x1"/>      

<!-- HS assignment Handset 1 connected to SIP account 1, Handset 2 connected to SIP account 2, .. -->
    <SYMB_ITEM ID="BS_Accounts.astAccounts[0].uiSendMask" class="symb_item" value="0x1"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[0].uiReceiveMask" class="symb_item" value="0x1"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[0].ucState" class="symb_item" value="0x1"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[1].uiSendMask" class="symb_item" value="0x2"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[1].uiReceiveMask" class="symb_item" value="0x2"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[1].ucState" class="symb_item" value="0x1"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[2].uiSendMask" class="symb_item" value="0x4"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[2].uiReceiveMask" class="symb_item" value="0x4"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[2].ucState" class="symb_item" value="0x1"/>	
    <SYMB_ITEM ID="BS_Accounts.astAccounts[3].uiSendMask" class="symb_item" value="0x8"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[3].uiReceiveMask" class="symb_item" value="0x8"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[3].ucState" class="symb_item" value="0x1"/>	
    <SYMB_ITEM ID="BS_Accounts.astAccounts[4].uiSendMask" class="symb_item" value="0x10"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[4].uiReceiveMask" class="symb_item" value="0x10"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[4].ucState" class="symb_item" value="0x1"/>	
    <SYMB_ITEM ID="BS_Accounts.astAccounts[5].uiSendMask" class="symb_item" value="0x20"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[5].uiReceiveMask" class="symb_item" value="0x20"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[5].ucState" class="symb_item" value="0x1"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[6].uiSendMask" class="symb_item" value="0x0"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[6].uiReceiveMask" class="symb_item" value="0x0"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[6].ucState" class="symb_item" value="0x1"/>    
    <SYMB_ITEM ID="BS_Accounts.astAccounts[7].uiSendMask" class="symb_item" value="0x0"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[7].uiReceiveMask" class="symb_item" value="0x0"/>
    <SYMB_ITEM ID="BS_Accounts.astAccounts[7].ucState" class="symb_item" value="0x1"/>    
<!-- end -->
    
  </Provider>
</ProviderFrame>

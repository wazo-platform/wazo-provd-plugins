<?xml version="1.0" encoding="ISO-8859-1"?>
<ProviderFrame xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="N720_general.xsd">
	<Provider>
    <!-- Please enter the correct MAC Address example: 3E2F800E1234
        Please enter correct Version value: DDMMYYHHMM example: 2811120928 Version Value field is optional and can be removed.
        Please enter a Profile name
        If not correct, no settings will be changed
    -->
        <MAC_ADDRESS value="{{ XX_mac_addr }}"/>
        <PROFILE_NAME class="string" value="N720"/>
    {# Disable firmware upgrade temporarily because of issues
    {%- if http_port %}
        <S_SPECIAL_DATA_SRV_IWU class="string" value='"http://{{ ip }}:{{ http_port }}/Gigaset/server_einstein_iwu111.bin"'/>
        <S_SPECIAL_DATA_SRV_SAT class="string" value='"http://{{ ip }}:{{ http_port }}/Gigaset/sat7111100000000.bin"'/>
    {%- endif %}
    #}
    <S_SPECIAL_DATA_SRV_IWU class="string" value=""/>
    <S_SPECIAL_DATA_SRV_SAT class="string" value=""/>
    <!-- NetDirectory settings -->
    {%- if XX_xivo_phonebook_url %}
        <SYMB_ITEM ID="BS_XML_Netdirs.aucAvailableNetdirs[%]" class="symb_item" value="0x2a"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.aucActivatedNetdirs[%]" class="symb_item" value="0x2a"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.aucNetdirSelForDirectAccess[%]" class="symb_item" value="0x2a"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.aucNetdirSelForIntKey[%]" class="symb_item" value="0x2a"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.aucNetdirSelForAutoLookup[%]" class="symb_item" value="0x0"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].aucProviderName[%]" class="symb_item" value='"WazoPBX"'/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].aucWhitePagesDirName[%]" class="symb_item" value='""'/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].aucYellowPagesDirName[%]" class="symb_item" value='""'/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].aucPrivatePagesDirName[%]" class="symb_item" value='"Contacts"'/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].aucUsername[%]" class="symb_item" value='""'/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].aucPassword[%]" class="symb_item" value='""'/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].aucServerURL[%]" class="symb_item" value='"{{ XX_xivo_phonebook_url }}"'/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].ucAuthPossibilities" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].aucCountryCode[%]" class="symb_item" value='""'/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].bitfldCap.bSearchPeopleCap" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].bitfldCap.bSearchBusinessCap" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].bitfldCap.bReverseSearchCap" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].bitfldCap.bAutolookupCap" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].bitfldCap.bPrivateDirectoryCap" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].bitfldCap.bPrivateDirectoryNicknameCap" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].bitfldCap.bSndMacAddress" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_XML_Netdirs.astNetdirProvider[0].bitfldCap.bEncryptPosts" class="symb_item" value="0"/>
    {%- endif %}

    <!-- Local settings - Data -->
        <SYMB_ITEM ID="BS_IP_Data.aucS_NETWORK_DEVICENAME[%]" class="symb_item" value='"N720-DM-PRO"'/>
    {%- if http_port %}
        <SYMB_ITEM ID="BS_IP_Data.aucS_DATA_SERVER[%]" class="symb_item" value='"http://{{ ip }}:{{ http_port }}"'/>
    {%- endif %}
        <SYMB_ITEM ID="BS_CUSTOM.bit.UseRandomRegistrationPIN" class="symb_item" value="0"/>
    	<SYMB_ITEM ID="BS_CUSTOM.aucKdsPin[%]" class="symb_item" value="0x00,0x00"/>
        <SYMB_ITEM ID="BS_IP_Data.ucB_USE_DHCP" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_IP_Data.ulI_IP" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_IP_Data.ulI_SUBNET_MASK" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_IP_Data.ulI_DEFAULT_ROUTER" class="symb_item" value="0"/>
    {%- if dns_enabled %}
        <SYMB_ITEM ID="BS_IP_Data.ulI_DNS_SERVER_1" class="symb_item" value="{{ XX_dns_ip_hex }}"/>
        <SYMB_ITEM ID="BS_IP_Data.ulI_DNS_SERVER_2" class="symb_item" value="0"/>
    {%- endif %}
        <SYMB_ITEM ID="BS_IP_Data.ulI_DHCP_ASSIGNED_IP" class="symb_item" value="0"/>
    {%- if vlan_enabled %}
        <SYMB_ITEM ID="BS_IP_Data.ucB_VLAN_ENABLED" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_IP_Data.ucI_VLAN_PRIORITY" class="symb_item" value="{{ vlan_priority }}"/>
        <SYMB_ITEM ID="BS_IP_Data.uiI_VLAN_ID" class="symb_item" value="{{ XX_vlan_id_hex }}"/>
    {%- endif %}
        <SYMB_ITEM ID="BS_IP_Data.uiI_PAGE_MASK_ID" class="symb_item" value="0xf0ff"/>
        <SYMB_ITEM ID="BS_IP_Data.ucB_AUTO_UPDATE_FW" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_IP_Data.ucI_REMINDER_FW_UPDATE" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_IP_Data.ucB_DO_CHECK_FOR_FIRMWARE_UPDATES" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_IP_Data.ucB_DO_CHECK_FOR_PROFILE_UPDATES" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_IP_Data.ucB_DO_CHECK_FOR_LANGUAGE_UPDATES" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_IP_Data.ucB_ACCEPT_FOREIGN_SUBNET" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_IP_Data.ucB_HTTP_PROXY_ENABLED" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_IP_Data.aucS_HTTP_PROXY_URL[%]" class="symb_item" value='""'/>
        <SYMB_ITEM ID="BS_IP_Data.uiI_HTTP_PROXY_PORT" class="symb_item" value="8080"/>
        <SYMB_ITEM ID="BS_IP_Data.ucI_HTTPLANGUAGE" class="symb_item" value="1"/>

    {%- if ntp_enabled %}
        <SYMB_ITEM ID="BS_IP_Data.aucS_TIME_NTP_SERVER[%]" class="symb_item" value='"{{ ntp_ip }}"'/>
        <SYMB_ITEM ID="BS_IP_Data.ucB_TIME_USE_AUTOMATIC_NTP_SYN" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_IP_Data.ulI_TIME_LAST_SYN" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_IP_Data.uiI_TIME_COUNTRY" class="symb_item" value="0xff"/><!-- TO CHANGE -->
        <SYMB_ITEM ID="BS_IP_Data.uiI_TIME_TIMEZONE" class="symb_item" value="0x{{ "%x"|format(XX_timezone_code) }}"/>
        <SYMB_ITEM ID="BS_IP_Data.ucB_TIME_USE_AUTOMATIC_DST" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_IP_Data.ucI_DIALING_PLAN_COUNTRY_ID" class="symb_item" value="0xff"/>
    {%- endif %}
        <SYMB_ITEM ID="BS_IP_Data.SystemBehindCelsiusPBX" class="symb_item" value="0"/>

    <!-- Settings for VOIP and SIP -->
        <SYMB_ITEM ID="BS_VOIP_Data.aucS_HOOK_FLASH_APPL_TYPE[%]" class="symb_item" value='"dtmf-relay"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.aucS_HOOK_FLASH_SIGNAL[%]" class="symb_item" value='"16"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.ucB_CTO_REFER_TO_PREFERRED_CONTACT" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_VOIP_Data.ucB_CTO_REFER_TO_AUTOMATIC" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_VOIP_Data.ucI_CNIP_STORE_STYLE" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_VOIP_Data.ucB_VOIP_CALLWAITING_STATUS" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_VOIP_Data.ucB_ATTENDED_CALL_TRANS_HOLD_TARGET" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_VOIP_Data.ucB_UNATTENDED_CALL_TRANS_HOLD_TARGET" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_VOIP_Data.ucB_USE_R_KEY_FOR_CALL_TRANSFER" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_VOIP_Data.uiI_SIP_LOCAL_PORT_MAX" class="symb_item" value="6000"/>
        <SYMB_ITEM ID="BS_VOIP_Data.uiI_RTP_LOCAL_PORT_MAX" class="symb_item" value="5024"/>

        {%- if sip_proxy_port %}
        <SYMB_ITEM ID="BS_VOIP_Data.uiI_SIP_LOCAL_PORT" class="symb_item" value="0x{{ "%x"|format(sip_proxy_port) }}"/>
        {%- endif %}

        <SYMB_ITEM ID="BS_VOIP_Data.uiI_RTP_LOCAL_PORT" class="symb_item" value="0x138c"/>
        <SYMB_ITEM ID="BS_VOIP_Data.ucB_USE_RANDOM_PORT" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[%].ucB_CALL_MANAGER_SUPPORT" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[%].ucI_CALL_MANAGER_ASSOCIATED_HANDSET" class="symb_item" value="0xff"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[%].ucB_CALL_MANAGER_SERVER_AUTH" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[%].aucS_AUTOPROVISIONING_CODE[%]" class="symb_item" value='"960"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[%].ucB_VOIP_CALLFORWARDING_STATUS" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[%].ucI_VOIP_CALLFORWARDING_WHEN" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[%].aucS_VOIP_CALLFORWARDING_NUMBER[%]" class="symb_item" value='""'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[%].aucS_VOIP_NET_AM_NUMBER_1[%]" class="symb_item" value='""'/>


    <!-- Genaral settings for 100 VoIP accounts-->
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[%].ucVoipProviderIndex" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].ucONESHOT_PROVISIONING_MODE_1" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].aucSIP_PROVIDER_NAME[%]" class="symb_item" value='"WazoPBX"'/>
        {%- if sip_proxy_ip %}
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].aucSIP_DOMAIN[%]" class="symb_item" value='"{{ sip_proxy_ip }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].aucSIP_SERVER[%]" class="symb_item" value='"{{ sip_proxy_ip }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].uiSIP_SERVER_PORT" class="symb_item" value="0x{{ "%x"|format(sip_proxy_port) }}"/>
        {%- endif %}

        {%- if exten_dnd %}
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[%].NetCodeDND_ON[%]" class="symb_item" value='"{{ exten_dnd }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[%].NetCodeDND_OFF[%]" class="symb_item" value='"{{ exten_dnd }}"'/>
        {%- endif %}

        {%- if exten_fwd_unconditional %}
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[%].NetCodeCFU_ON[%]" class="symb_item" value='"{{ exten_fwd_unconditional }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[%].NetCodeCFU_OFF[%]" class="symb_item" value='"{{ exten_fwd_unconditional }}"'/>
        {%- endif %}

        {%- if exten_fwd_busy %}
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[%].NetCodeCFB_ON[%]" class="symb_item" value='"{{ exten_fwd_busy }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[%].NetCodeCFB_OFF[%]" class="symb_item" value='"{{ exten_fwd_busy }}"'/>
        {%- endif %}

        {%- if exten_fwd_no_answer %}
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[%].NetCodeCFNR_ON[%]" class="symb_item" value='"{{ exten_fwd_no_answer }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[%].NetCodeCFNR_OFF[%]" class="symb_item" value='"{{ exten_fwd_no_answer }}"'/>
        {%- endif %}

        {%- if sip_registrar_ip %}
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].aucSIP_REGISTRAR[%]" class="symb_item" value='"{{ sip_registrar_ip }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].uiSIP_REGISTRAR_PORT" class="symb_item" value="0x{{ "%x"|format(sip_registrar_port) }}"/>
        {%- endif %}

        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].uiRE_REGISTRATION_TIMER" class="symb_item" value="0x00B4"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].ucSIP_USE_STUN" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].aucSTUN_SERVER[%]" class="symb_item" value='""'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].uiSTUN_SERVER_PORT" class="symb_item" value="0x0d96"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].uiRE_STUN_TIMER" class="symb_item" value="0x00F0"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].uiNAT_REFRESH_TIME" class="symb_item" value="0x0014"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].ucOUTBOUND_PROXY_MODE" class="symb_item" value="2"/>

        {%- if sip_outbound_proxy_ip %}
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].aucOUTBOUND_PROXY[%]" class="symb_item" value='"{{ sip_outbound_proxy_ip }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].uiOUTBOUND_PROXY_PORT" class="symb_item" value="0x{{ "%x"|format(sip_outbound_proxy_port) }}"/>
        {%- endif %}

        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].aucCURRENT_PROFILE_NAME[0]" class="symb_item" value='"wazopbx"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].ulCURRENT_PROFILE_DATE" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].ucSH_SHOW_USER_NAME" class="symb_item" value="1"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].aucSH_AUTH_NAME_LABEL[%]" class="symb_item" value='""'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].aucSH_AUTH_PASS_LABEL[%]" class="symb_item" value='""'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].aucSH_USER_NAME_LABEL[%]" class="symb_item" value='""'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipProviders[0].ucSIP_PREFERRED_TRANSPORT_LAYER" class="symb_item" value="17"/> <!-- UDP -->
        <SYMB_ITEM ID="BS_VOIP_Data.ucI_DTMF_TX_RTP_PAYLOAD_TYPE" class="symb_item" value="0x65"/>
        <SYMB_ITEM ID="BS_VOIP_Data.ucB_DTMF_TX_MODE_AUTO" class="symb_item" value="1"/>

    <!--Bit-Masks for I_DTMF_TX_MODE_BITS: Audio=1, RFC2833=2, SIP-INFO=4
            <SYMB_ITEM ID="BS_VOIP_Data.ucI_DTMF_TX_MODE_BITS" class="symb_item" value="1"/>
    -->
        <SYMB_ITEM ID="BS_VOIP_Data.ucI_SIP_AVAILABLE_VOCODER[%]" class="symb_item" value="0x01,0x00,0x02,0x03,0x05"/>
        <SYMB_ITEM ID="BS_VOIP_Data.ucI_SIP_PREDEFINED_VOCODER[%]" class="symb_item" value="0x05,0x00,0x01,0x02,0x03"/>
        <SYMB_ITEM ID="BS_VOIP_Data.ucI_SIP_LOW_BANDWIDTH_VOCODER[%]" class="symb_item" value="0x03,0x02,0x01,0x00,0x05"/>
        <SYMB_ITEM ID="BS_VOIP_Data.ucI_SIP_HIGH_BANDWIDTH_VOCODER[%]" class="symb_item" value="0x05,0x00,0x01,0x02,0x03"/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[%].aucI_SIP_PREFERRED_VOCODER[%]" class="symb_item" value="0x01,0x00,0x02,0x05,0xff"/>
        <SYMB_ITEM ID="BS_VOIP_Data.EnableWideband" class="symb_item" value="0"/>
        <SYMB_ITEM ID="BS_VOIP_Data.NameOnIdleDisplay" class="symb_item" value="1"/>
    <!--VoIP 1 -->

    {%- if sip_lines %}
        {%- for line_no, line in sip_lines.iteritems() %}
        {%- set lnb = line_no|int() - 1 %}
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[{{ lnb }}].aucS_SIP_DISPLAYNAME[0]" class="symb_item" value='"{{ line['number'] }} | {{ line['display_name'] }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[{{ lnb }}].aucS_SIP_LOGIN_ID[0]" class="symb_item" value='"{{ line['auth_username']|d(line['username']) }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[{{ lnb }}].aucS_SIP_PASSWORD[0]" class="symb_item" value='"{{ line['auth_password']|d(line['password']) }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[{{ lnb }}].aucS_SIP_USER_ID[0]" class="symb_item" value='"{{ line['auth_username']|d(line['username']) }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[{{ lnb }}].ucB_SIP_ACCOUNT_IS_ACTIVE_1" class="symb_item" value="1"/>
        {%- if exten_voicemail %}
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[{{ lnb }}].aucS_VOIP_NET_AM_NUMBER_1[%]" class="symb_item" value='"{{ exten_voicemail }}"'/>
        <SYMB_ITEM ID="BS_VOIP_Data.astVoipAccounts[{{ lnb }}].ucB_VOIP_NET_AM_ENABLED_1" class="symb_item" value="1"/>
        {%- endif %}

        {%- endfor %}
    {%- endif %}
    </Provider>
</ProviderFrame>

<?xml version="1.0" encoding="UTF-8" ?>
<hl_provision version="1">
    <config version="1">
    <!--Profile1/Basic-->
        <P47 para="Profile1_Sipserver">{{ sip_lines['1']['proxy_ip'] }}:{{ sip_lines['1']['proxy_port']|d('5060') }}</P47>
      {%- if sip_lines['1']['backup_proxy_ip'] %}
        <P967 para="Profile1_FailoverSipserver">{{ sip_lines['1']['backup_proxy_ip'] }}:{{ sip_lines['1']['backup_proxy_port']|d('5060') }}</P967>
      {%- endif %}
        <P8851 para="Profile1_SecondFailoverSipserver" />
        <P4567 para="Profile1_PreferPrimaryServer">0</P4567>
      {%- if sip_lines['1']['outbound_proxy_ip'] %}
        <P48 para="Profile1_OutboundProxy">{{ sip_lines['1']['outbound_proxy_ip'] }}:{{ sip_lines['1']['outbound_proxy_port']|d('5060') }}</P48>
      {%- endif %}
        <P20047 para="Profile1_BackUpOutboundProxy" />
        <P130 para="Profile1_SipTransport">{{ XX_sip_transport }}</P130>
        <P52 para="Profile1_NatTraversal">2</P52>
        <P103 para="Profile1_DnsMode">0</P103>
        <P63 para="Profile1_UserIdIsPhoneNumber">0</P63>
        <P31 para="Profile1_SipRegistration">1</P31>
        <P81 para="Profile1_UnregisterOnReboot">1</P81>
        <P32 para="Profile1_RegisterExpiration">1</P32>
        <P109 para="Profile1_OutCallWithoutReg">0</P109>
        <P136 para="Profile1_RPort">0</P136>
        <P1100 para="Profile1_RFC2543Hold">1</P1100>
        <P8775 para="Profile1_ConnectMode">0</P8775>
        <!--Profile1/Codec-->
        <P57 para="Profile1_Choice1">0</P57>
        <P58 para="Profile1_Choice2">8</P58>
        <P59 para="Profile1_Choice3">9</P59>
        <P60 para="Profile1_Choice4">20</P60>
        <P61 para="Profile1_Choice5">120</P61>
        <P62 para="Profile1_Choice6">2</P62>
        <P37 para="Profile1_VoiceFramesPerTX">2</P37>
        <P49 para="Profile1_G723Rate">0</P49>
        <P394 para="Profile1_LibcMode">0</P394>
        <P390 para="Profile1_LibcPayloadType">97</P390>
        <P402 para="Profile1_OPUSPayloadType">120</P402>
        <P24066 para="Profile1_G72632CustomOnoff">0</P24066>
        <P24072 para="Profile1_G72632CustomPayloadType">111</P24072>
        <!--Profile1/Advance-->
        <P79 para="Profile1_DtmfPayloadType">101</P79>
        <P20166 para="Profile1_DtmfMode">{{ sip_lines['1']['XX_dtmf_type'] }}</P20166>
        <P74 para="Profile1_SendFlashEvent">0</P74>
        <P191 para="Profile1_EnableCallFeatures">0</P191>
        <P197 para="Profile1_ProxyRequire" />
        <P101 para="Profile1_UseNatIP" />
        <P183 para="Profile1_SRtpMode">0</P183>
        <P50 para="Profile1_VAD">0</P50>
        <P291 para="Profile1_SymmetricRTP">0</P291>
        <P133 para="Profile1_JitterBufferType">1</P133>
        <P132 para="Profile1_JitterBufferLength">1</P132>
        <P104 para="Profile1_AccountRingTone">0</P104>
        <P185 para="Profile1_RingTimeout">60</P185>
        <P99 para="Profile1_SubscribeForMWI">1</P99>
        <P24759 para="Profile1_SubscribeMWIToVoiceMail">0</P24759>
        <P65 para="Profile1_SendAnonymous">0</P65>
        <P129 para="Profile1_AnonymousCallRejection">0</P129>
        <P258 para="Profile1_CheckSIPUserID">0</P258>
        <P90 para="Profile1_AutoAnswer">0</P90>
        <P298 para="Profile1_AnswerViaCallInfo">1</P298>
        <P299 para="Profile1_OffSpeakerDisconnect">1</P299>
        <P260 para="Profile1_SessionExpiration">180</P260>
        <P261 para="Profile1_MinSE">90</P261>
        <P262 para="Profile1_CallerRequestTimer">0</P262>
        <P263 para="Profile1_CalleeRequestTimer">0</P263>
        <P264 para="Profile1_ForceTimer">0</P264>
        <P266 para="Profile1_UACSpecifyRefresher">0</P266>
        <P267 para="Profile1_UASSpecifyRefresher">1</P267>
        <P265 para="Profile1_ForceINVITE">0</P265>
        <P251 para="Profile1_HookFlashMinTiming">50</P251>
        <P252 para="Profile1_HookFlashMaxTiming">100</P252>
        <P198 para="Profile1_SpecialFeature">100</P198>
        <P8791 para="Profile1_SIPServerType">0</P8791>
        <P8811 para="Profile1_100rel">0</P8811>
        <P8841 para="Profile1_EarlySession">0</P8841>
        <P8845 para="Profile1_RefuseReturnCode">0</P8845>
        <P20004 para="Profile1_ConferenceType">0</P20004>
        <P20008 para="Profile1_ConferenceURI" />
        <P20053 para="Profile1_SipSendMac">1</P20053>
        <P20157 para="Profile1_CallerDisplaySource">0</P20157>
        <P20970 para="Profile1_SubscribeExpires">300</P20970>
        <P851 para="Profile1_DTMFVia2833">0</P851>
        <P850 para="Profile1_DTMFInAudio">0</P850>
        <P852 para="Profile1_DTMFViaSipInfo">1</P852>
        <P24785 para="Profile1_TrsRelSetting">0</P24785>
        <P72 para="Preference_UsePoundAsDialKey">1</P72>

        <P331 para="PhonebookXmlDownload_ServerPath">{{ XX_xivo_phonebook_url }}</P331>
        <P332 para="PhonebookXmlDownload_Interval">0</P332>
        <P333 para="PhonebookXmlDownload_RemoveMEOnDownload">0</P333>
        <P330 para="PhonebookXmlDownload_Enable">1</P330>
      {%- if '1' in sip_lines %}
      {%- set line = sip_lines['1'] %}
        <!--Account1/Basic-->
        <P271 para="Account1_Active">1</P271>
        <P24082 para="Account1_Profile">0</P24082>
        <P20000 para="Account1_Label">{{ line['number'] }}</P20000>
        <P35 para="Account1_SipUserId">{{ line['username'] }}</P35>
        <P36 para="Account1_AuthenticateID">{{ line['auth_username'] }}</P36>
        <P34 para="Account1_AuthenticatePassword">{{ line['password'] }}</P34>
        <P3 para="Account1_DispalyName">{{ line['display_name'] }}</P3>
        <P78 para="Account1_UseRandomPort">1</P78>
        <P33 para="Account1_VoiceMailId">{{ line['voicemail'] }}</P33>
        <P4200 para="Account1_DialPlan">{[x*]+}</P4200>
        {%- if exten_pickup_call %}
        <P4705 para="Account1_DirectCallPickupCode">{{ exten_pickup_call }}</P4705>
        {%- endif %}
        {%- if exten_pickup_group %}
        <P4706 para="Account1_GroupCallPickupCode">{{ exten_pickup_group }}</P4706>
        {%- endif %}
      {%- endif %}
      {%- if '2' in sip_lines %}
      {%- set line = sip_lines['2'] %}
        <!--Account2/Basic-->
        <P401 para="Account2_Active">1</P401>
        <P24083 para="Account2_Profile">0</P24083>
        <P20001 para="Account2_Label">{{ line['number'] }}</P20001>
        <P735 para="Account2_SipUserId">{{ line['username'] }}</P735>
        <P736 para="Account2_AuthenticateID">{{ line['auth_username'] }}</P736>
        <P734 para="Account2_AuthenticatePassword">{{ line['password'] }}</P734>
        <P703 para="Account2_DispalyName">{{ line['display_name'] }}</P703>
        <P778 para="Account2_UseRandomPort">1</P778>
        <P426 para="Account2_VoiceMailId">{{ line['voicemail'] }}</P426>
        <P4201 para="Account2_DialPlan">{[x*]+}</P4201>
        {%- if exten_pickup_call %}
        <P4715 para="Account2_DirectCallPickupCode">{{ exten_pickup_call }}</P4715>
        {%- endif %}
        {%- if exten_pickup_group %}
        <P4716 para="Account2_GroupCallPickupCode">{{ exten_pickup_group }}</P4716>
        {%- endif %}
      {%- endif %}
      {%- if '3' in sip_lines %}
      {%- set line = sip_lines['3'] %}
        <!--Account3/Basic-->
        <P501 para="Account3_Active">1</P501>
        <P24084 para="Account3_Profile">0</P24084>
        <P20002 para="Account3_Label">{{ line['number'] }}</P20002>
        <P504 para="Account3_SipUserId">{{ line['username'] }}</P504>
        <P505 para="Account3_AuthenticateID">{{ line['auth_username'] }}</P505>
        <P506 para="Account3_AuthenticatePassword">{{ line['password'] }}</P506>
        <P507 para="Account3_DispalyName">{{ line['display_name'] }}</P507>
        <P578 para="Account3_UseRandomPort">1</P578>
        <P526 para="Account3_VoiceMailId">{{ line['voicemail'] }}</P526>
        <P4202 para="Account3_DialPlan">{[x*]+}</P4202>
        {%- if exten_pickup_call %}
        <P4725 para="Account3_DirectCallPickupCode">{{ exten_pickup_call }}</P4725>
        {%- endif %}
        {%- if exten_pickup_group %}
        <P4726 para="Account3_GroupCallPickupCode">{{ exten_pickup_group }}</P4726>
        {%- endif %}
      {%- endif %}
      {%- if '4' in sip_lines %}
      {%- set line = sip_lines['4'] %}
        <!--Account4/Basic-->
        <P601 para="Account4_Active">1</P601>
        <P24085 para="Account4_Profile">0</P24085>
        <P20003 para="Account4_Label">{{ line['number'] }}</P20003>
        <P604 para="Account4_SipUserId">{{ line['username'] }}</P604>
        <P605 para="Account4_AuthenticateID">{{ line['auth_username'] }}</P605>
        <P606 para="Account4_AuthenticatePassword">{{ line['password'] }}</P606>
        <P607 para="Account4_DispalyName">{{ line['display_name'] }}</P607>
        <P678 para="Account4_UseRandomPort">1</P678>
        <P626 para="Account4_VoiceMailId">{{ line['voicemail'] }}</P626>
        <P4203 para="Account4_DialPlan">{[x*]+}</P4203>
        {%- if exten_pickup_call %}
        <P4735 para="Account4_DirectCallPickupCode">{{ exten_pickup_call }}</P4735>
        {%- endif %}
        {%- if exten_pickup_group %}
        <P4736 para="Account4_GroupCallPickupCode">{{ exten_pickup_group }}</P4736>
        {%- endif %}
      {%- endif %}
      {%- if '5' in sip_lines %}
      {%- set line = sip_lines['5'] %}
        <!--Account5/Basic-->
        <P20360 para="Account5_Active">1</P20360>
        <P24086 para="Account5_Profile">4</P24086>
        <P20378 para="Account5_Label">{{ line['number'] }}</P20378>
        <P1704 para="Account5_SipUserId">{{ line['username'] }}</P1704>
        <P1705 para="Account5_AuthenticateID">{{ line['auth_username'] }}</P1705>
        <P1706 para="Account5_AuthenticatePassword">{{ line['password'] }}</P1706>
        <P1707 para="Account5_DispalyName">{{ line['display_name'] }}</P1707>
        <P20390 para="Account5_UseRandomPort">1</P20390>
        <P1726 para="Account5_VoiceMailId">{{ line['voicemail'] }}</P1726>
        <P4204 para="Account5_DialPlan">{[x*]+}</P4204>
        {%- if exten_pickup_call %}
        <P20464 para="Account5_DirectCallPickupCode">{{ exten_pickup_call }}</P20464>
        {%- endif %}
        {%- if exten_pickup_group %}
        <P20466 para="Account5_GroupCallPickupCode">{{ exten_pickup_group }}</P20466>
        {%- endif %}
      {%- endif %}
      {%- if '6' in sip_lines %}
      {%- set line = sip_lines['6'] %}
        <!--Account6/Basic-->
        <P20361 para="Account6_Active">1</P20361>
        <P24087 para="Account6_Profile">5</P24087>
        <P20379 para="Account6_Label">{{ line['number'] }}</P20379>
        <P1804 para="Account6_SipUserId">{{ line['username'] }}</P1804>
        <P1805 para="Account6_AuthenticateID">{{ line['auth_username'] }}</P1805>
        <P1806 para="Account6_AuthenticatePassword">{{ line['password'] }}</P1806>
        <P1807 para="Account6_DispalyName">{{ line['display_name'] }}</P1807>
        <P20391 para="Account6_UseRandomPort">1</P20391>
        <P1826 para="Account6_VoiceMailId">{{ line['voicemail'] }}</P1826>
        <P4205 para="Account6_DialPlan">{[x*]+}</P4205>
        {%- if exten_pickup_call %}
        <P20465 para="Account6_DirectCallPickupCode">{{ exten_pickup_call }}</P20465>
        {%- endif %}
        {%- if exten_pickup_group %}
        <P20467 para="Account6_GroupCallPickupCode">{{ exten_pickup_group }}</P20467>
        {%- endif %}
      {%- endif %}
      {%- for line_no in range(7, 17) %}
      {%- set inc = line_no - 7 %}
      {%- if line_no|string() in sip_lines %}
        {%- set line = sip_lines[line_no|string()] %}
        <!--Account{{ line_no }}/Basic-->
        <P{{ 24090 + inc }} para="Account{{ line_no }}_Active">1</P{{ 24090 + inc }}>
        <P{{ 24088 + inc }} para="Account{{ line_no }}_Profile">0</P{{ 24088 + inc }}>
        <P{{ 24100 + inc }} para="Account{{ line_no }}_Label">{{ line['number'] }}</P{{ 24100 + inc }}>
        <P{{ 24110 + inc }} para="Account{{ line_no }}_SipUserId">{{ line['username'] }}</P{{ 24110 + inc }}>
        <P{{ 24120 + inc }} para="Account{{ line_no }}_AuthenticateID">{{ line['auth_username'] }}</P{{ 24120 + inc }}>
        <P{{ 24130 + inc }} para="Account{{ line_no }}_AuthenticatePassword">{{ line['password'] }}</P{{ 24130 + inc }}>
        <P{{ 24140 + inc }} para="Account{{ line_no }}_DispalyName">{{ line['display_name'] }}</P{{ 24140 + inc }}>
        <P{{ 24160 + inc }} para="Account{{ line_no }}_UseRandomPort">1</P{{ 24160 + inc }}>
        <P{{ 24170 + inc }} para="Account{{ line_no }}_VoiceMailId">{{ line['voicemail'] }}</P{{ 24170 + inc }}>
        <P{{ 24180 + inc }} para="Account{{ line_no }}_DialPlan">{[x*]+}</P{{ 24180 + inc }}>
        {%- if exten_pickup_call %}
        <P{{ 24220 + inc }} para="Account{{ line_no }}_DirectCallPickupCode">{{ exten_pickup_call }}</P{{ 24220 + inc }}>
        {%- endif %}
        {%- if exten_pickup_group %}
        <P{{ 24230 + inc }} para="Account{{ line_no }}_GroupCallPickupCode">{{ exten_pickup_group }}</P{{ 24230 + inc }}>
        {%- endif %}
      {%- endif %}
      {%- endfor %}
        <!--Network/Basic-->
        <P8 para="IPv4WanMode">0</P8>
        <P190 para="HttpAccess">1</P190>
        <P112 para="IPLeaseTime">24</P112>
        <P8639 para="DhcpServerFlag">0</P8639>
        <!--Network/Advance-->
        <!--Network/Advance/LLDP-->
        <P5438 para="Active">0</P5438>
        <P5439 para="PackedInterval">120</P5439>
        <!--Network/Advance/Qos Set -->
        <P38 para="Layer3QoS">48</P38>
        <!--Network/Advance/NTP Server-->
        <P30 para="UrlOrIpAddress">{{ ntp_ip|d('pool.ntp.org') }}</P30>
        <P64 para="Preference_TimeZone">{{ XX_timezone_code }}</P64>
        <P143 para="Preference_DHCPTime">0</P143>
        <P75 para="Preference_DaylightSavingTime">2</P75>
        <!--Setting/Features-->
      {%- if vlan_enabled %}
        <P24053 para="Network_Advanced_Vlan_WANVlan">1</P24053>
        <P229 para="DataVLANTag">{{ vlan_id }}</P229>
        <P51 para="Layer2QoS_802_1Q_VLANTag">{{ vlan_id }}</P51>
        <P87 para="Layer2QoS_802_1pPriorityValue">{{ vlan_priority|d(0) }}</P87>
      {%- else %}
        <P24053 para="Network_Advanced_Vlan_WANVlan">0</P24053>
        <P229 para="DataVLANTag">0</P229>
        <P51 para="Layer2QoS_802_1Q_VLANTag">0</P51>
        <P87 para="Layer2QoS_802_1pPriorityValue">0</P87>
      {%- endif %}

        <P3201 para="Transfer_BlindTransferOnHook">1</P3201>
        <P3202 para="Transfer_Semi_AttendedTransfer">1</P3202>
        <P3204 para="Transfer_AttendedTransferOnHook">0</P3204>

        <!--Directory-->
        <!--Directory/RemotePhoneBook-->
        <P4401 para="RemotePhoneBook1_Url">{{ XX_xivo_phonebook_url }}&term=</P4401>
        <P3316 para="RemotePhoneBook1_Name">Wazo</P3316>
        <P4402 para="RemotePhoneBook2_Url" />
        <P3312 para="RemotePhoneBook2_Name" />
        <P4403 para="RemotePhoneBook3_Url" />
        <P3313 para="RemotePhoneBook3_Name" />
        <P4404 para="RemotePhoneBook4_Url" />
        <P3314 para="RemotePhoneBook4_Name" />
        <P4405 para="RemotePhoneBook5_Url" />
        <P3315 para="RemotePhoneBook5_Name" />

        <!--FunctionKeys/ProgrammableKey-->
        <P43200 para="SoftKey1_Type">36</P43200>
        <P43300 para="SoftKey1_Account">255</P43300>
        <P43400 para="SoftKey1_Value" />
        <P43201 para="SoftKey2_Type">16</P43201>
        <P43301 para="SoftKey2_Account">255</P43301>
        <P43401 para="SoftKey2_Value" />
        <P43202 para="SoftKey3_Type">21</P43202>
        <P43302 para="SoftKey3_Account">255</P43302>
        <P43402 para="SoftKey3_Value" />
        <P43203 para="SoftKey4_Type">38</P43203>
        <P43303 para="SoftKey4_Account">255</P43303>
        <P43403 para="SoftKey4_Value" />

        <P20043 para="ProgrammableKey1_Label" />
        <P20044 para="ProgrammableKey2_Label">Contacts</P20044>
        <P20045 para="ProgrammableKey3_Label" />
        <P20046 para="ProgrammableKey4_Label" />
      {%- if XX_fkeys %}
        <!--FunctionKeys/LineKeys-->
        {%- for fnkey, value in XX_fkeys|dictsort(by='key') %}
        <P{{ value['type']['p_nb'] }} para="LineKey{{ fnkey }}_Type">{{ value['type']['val'] }}</P{{ value['type']['p_nb'] }}>
        <P{{ value['mode']['p_nb'] }} para="LineKey{{ fnkey }}_Mode">0</P{{ value['mode']['p_nb'] }}>
        <P{{ value['value']['p_nb'] }} para="LineKey{{ fnkey }}_Value">{{ value['value']['val'] }}</P{{ value['value']['p_nb'] }}>
        <P{{ value['label']['p_nb'] }} para="LineKey{{ fnkey }}_Label">{{ value['label']['val'] }}</P{{ value['label']['p_nb'] }}>
        <P{{ value['account']['p_nb'] }} para="LineKey{{ fnkey }}_Account">255</P{{ value['account']['p_nb'] }}>
        <P{{ value['extension']['p_nb'] }} para="LineKey{{ fnkey }}_Extension">{{ value['extension']['val'] }}</P{{ value['extension']['p_nb'] }}>
        {%- endfor %}
      {%- endif %}
      {%- block extra %}{% endblock %}
    </config>
</hl_provision>

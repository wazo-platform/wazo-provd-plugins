<?xml version="1.0" encoding="UTF-8" ?>
<hl_provision version="1">
    <config version="1">
      {% for line_no, line in XX_sip_lines.iteritems() -%}
        {% if line -%}
        <!--Account{{ line_no }}/Basic-->
        <P271 para="Account{{ line_no }}.Active">1</P271>
        <P47 para="Account{{ line_no }}.Sipserver">{{ line['proxy_ip'] }}</P47>
        <P967 para="Account{{ line_no }}.FailoverSipserver" />
        <P8851 para="Account{{ line_no }}.SecondFailoverSipserver" />
        <P4567 para="Account{{ line_no }}.PreferPrimaryServer">0</P4567>
        <P48 para="Account{{ line_no }}.OutboundProxy">{{ line['proxy_ip'] }}</P48>
        <P20047 para="Account{{ line_no }}.BackUpOutboundProxy" />
        <P130 para="Account{{ line_no }}.SipTransport">1</P130>
        <P52 para="Account{{ line_no }}.NatTraversal">2</P52>
        <P20000 para="Account{{ line_no }}.Label">{{ line['display_name'] }}</P20000>
        <P35 para="Account{{ line_no }}.SipUserId">{{ line['username'] }}</P35>
        <P36 para="Account{{ line_no }}.AuthenticateID">{{ line['auth_username'] }}</P36>
        <P34 para="Account{{ line_no }}.AuthenticatePassword">{{ line['password'] }}</P34>
        <P3 para="Account{{ line_no }}.DisplayName">{{ line['display_name'] }}</P3>
        <P103 para="Account{{ line_no }}.DnsMode">0</P103>
        <P63 para="Account{{ line_no }}.UserIdIsPhoneNumber">0</P63>
        <P31 para="Account{{ line_no }}.SipRegistration">1</P31>
        <P81 para="Account{{ line_no }}.UnregisterOnReboot">0</P81>
        <P32 para="Account{{ line_no }}.RegisterExpiration">1</P32>
        <P109 para="Account{{ line_no }}.OutCallWithoutReg">0</P109>
        <P40 para="Account{{ line_no }}.LocalSipPort">{{ line['proxy_port']|d('%NULL%') }}</P40>
        <P78 para="Account{{ line_no }}.UseRandomPort">0</P78>
        <P33 para="Account{{ line_no }}.VoiceMailId">{{ line['voicemail']|d('%NULL%') }}</P33>
        <P136 para="Account{{ line_no }}.RPort">cn</P136>
        <P1100 para="Account{{ line_no }}.RFC2543Hold">1</P1100>
        <P8775 para="Account{{ line_no }}.ConnectMode">0</P8775>
        <!--Account{{ line_no }}/Codec-->
        <P57 para="Account{{ line_no }}.Choice1">0</P57>
        <P58 para="Account{{ line_no }}.Choice2">8</P58>
        <P59 para="Account{{ line_no }}.Choice3">18</P59>
        <P60 para="Account{{ line_no }}.Choice4">2</P60>
        <P61 para="Account{{ line_no }}.Choice5">4</P61>
        <P62 para="Account{{ line_no }}.Choice6">9</P62>
        <P37 para="Account{{ line_no }}.VoiceFramesPerTX">2</P37>
        <P49 para="Account{{ line_no }}.G723Rate">0</P49>
        <P394 para="Account{{ line_no }}.LibcMode">0</P394>
        <P390 para="Account{{ line_no }}.LibcPayloadType">97</P390>
        <!--Account{{ line_no }}/Advance-->
        <P79 para="Account{{ line_no }}.DtmfPayloadType">101</P79>
        <P20166 para="Account{{ line_no }}.DtmfMode">0</P20166>
        <P74 para="Account{{ line_no }}.SendFlashEvent">0</P74>
        <P191 para="Account{{ line_no }}.EnableCallFeatures">0</P191>
        <P197 para="Account{{ line_no }}.ProxyRequire" />
        <P101 para="Account{{ line_no }}.UseNatIP" />
        <P183 para="Account{{ line_no }}.SRtpMode">0</P183>
        <P50 para="Account{{ line_no }}.VAD">0</P50>
        <P291 para="Account{{ line_no }}.SymmetricRTP">0</P291>
        <P133 para="Account{{ line_no }}.JitterBufferType">1</P133>
        <P132 para="Account{{ line_no }}.JitterBufferLength">1</P132>
        <P104 para="Account{{ line_no }}.AccountRingTone">0</P104>
        <P185 para="Account{{ line_no }}.RingTimeout">60</P185>
        <P72 para="Account{{ line_no }}.Use#AsDialKey">1</P72>
        <P4200 para="Account{{ line_no }}.DialPlan">{[x*]+}</P4200>
        <P99 para="Account{{ line_no }}.SubscribeForMWI">1</P99>
        <P65 para="Account{{ line_no }}.SendAnonymous">0</P65>
        <P129 para="Account{{ line_no }}.AnonymousCallRejection">0</P129>
        <P258 para="Account{{ line_no }}.CheckSIPUserID">0</P258>
        <P90 para="Account{{ line_no }}.AutoAnswer">0</P90>
        <P298 para="Account{{ line_no }}.AnswerViaCallInfo">1</P298>
        <P299 para="Account{{ line_no }}.OffSpeakerDisconnect">1</P299>
        <P260 para="Account{{ line_no }}.SessionExpiration">180</P260>
        <P261 para="Account{{ line_no }}.MinSE">90</P261>
        <P262 para="Account{{ line_no }}.CallerRequestTimer">0</P262>
        <P263 para="Account{{ line_no }}.CalleeRequestTimer">0</P263>
        <P264 para="Account{{ line_no }}.ForceTimer">0</P264>
        <P266 para="Account{{ line_no }}.UACSpecifyRefresher">0</P266>
        <P267 para="Account{{ line_no }}.UASSpecifyRefresher">1</P267>
        <P265 para="Account{{ line_no }}.ForceINVITE">0</P265>
        <P251 para="Account{{ line_no }}.HookFlashMinTiming">30</P251>
        <P252 para="Account{{ line_no }}.HookFlashMaxTiming">100</P252>
        <P198 para="Account{{ line_no }}.SpecialFeature">100</P198>
        <P134 para="Account{{ line_no }}.EventlistBlfUrl" />
        <P8771 para="Account{{ line_no }}.ShareLine">0</P8771>
        <P8791 para="Account{{ line_no }}.SIPServerType">0</P8791>
        <P8811 para="Account{{ line_no }}.100rel">0</P8811>
        <P8841 para="Account{{ line_no }}.EarlySession">0</P8841>
        <P8845 para="Account{{ line_no }}.RefuseReturnCode">0</P8845>
        <P4705 para="Account{{ line_no }}.DirectCallPickupCode" />
        <P4706 para="Account{{ line_no }}.GroupCallPickupCode" />
        <P20053 para="Account{{ line_no }}.SipSendMac">1</P20053>
        <P20157 para="Account{{ line_no }}.CallerDisplaySource">0</P20157>
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
        <P51 para="Layer2QoS.802.1Q/VLANTag">0</P51>
        <P87 para="Layer2QoS.802.1pPriorityValue">0</P87>
        <P229 para="DataVLANTag">0</P229>
        <!--Network/Advance/NTP Server-->
        <P30 para="UrlOrIpAddress">{{ ntp_ip|d('pool.ntp.org') }}</P30>
        <P144 para="DHCPOverrideNTP">0</P144>
    </config>
</hl_provision>

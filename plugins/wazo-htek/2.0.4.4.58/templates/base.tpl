<?xml version="1.0" encoding="UTF-8" ?>
<hl_provision version="1">
    <config version="1">
      {% for line_no, line in sip_lines.iteritems() -%}
        {% if line -%}
        <!--Account{{ line_no }}/Basic-->
        <P271 para="Account{{ line_no }}.Active">1</P271>
        <P47 para="Account{{ line_no }}.Sipserver">{{ line['proxy_ip'] }}:{{ line['proxy_port']|d('5060') }}</P47>
        {% if line['backup_proxy_ip'] -%}
        <P967 para="Account{{ line_no }}.FailoverSipserver">{{ line['backup_proxy_ip'] }}:{{ line['backup_proxy_port']|d('5060') }}</P967>
        {% endif -%}
        <P4567 para="Account{{ line_no }}.PreferPrimaryServer">0</P4567>
        <P130 para="Account{{ line_no }}.SipTransport">{{ XX_sip_transport }}</P130>
        <P52 para="Account{{ line_no }}.NatTraversal">2</P52>
        <P20000 para="Account{{ line_no }}.Label">{{ line['display_name'] }}</P20000>
        <P35 para="Account{{ line_no }}.SipUserId">{{ line['username'] }}</P35>
        <P36 para="Account{{ line_no }}.AuthenticateID">{{ line['auth_username'] }}</P36>
        <P34 para="Account{{ line_no }}.AuthenticatePassword">{{ line['password'] }}</P34>
        <P3 para="Account{{ line_no }}.DisplayName">{{ line['display_name'] }}</P3>
        <P103 para="Account{{ line_no }}.DnsMode">0</P103>
        <P63 para="Account{{ line_no }}.UserIdIsPhoneNumber">0</P63>
        <P31 para="Account{{ line_no }}.SipRegistration">1</P31>
        <P81 para="Account{{ line_no }}.UnregisterOnReboot">1</P81>
        <P32 para="Account{{ line_no }}.RegisterExpiration">1</P32>
        <P109 para="Account{{ line_no }}.OutCallWithoutReg">0</P109>
        <P78 para="Account{{ line_no }}.UseRandomPort">1</P78>
        <P33 para="Account{{ line_no }}.VoiceMailId">{{ line['voicemail'] }}</P33>
        <P1100 para="Account{{ line_no }}.RFC2543Hold">1</P1100>
        <!--Account{{ line_no }}/Advance-->
        <P79 para="Account{{ line_no }}.DtmfPayloadType">101</P79>
        <P20166 para="Account{{ line_no }}.DtmfMode">{{ line['XX_dtmf_type'] }}</P20166>
        <P191 para="Account{{ line_no }}.EnableCallFeatures">0</P191>
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
        <P20053 para="Account{{ line_no }}.SipSendMac">1</P20053>
        <P20157 para="Account{{ line_no }}.CallerDisplaySource">0</P20157>
        {% endif -%}
      {% endfor -%}
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
        {# TODO, we have config for that #}
        <P51 para="Layer2QoS.802.1Q/VLANTag">0</P51>
        <P87 para="Layer2QoS.802.1pPriorityValue">0</P87>
        <P229 para="DataVLANTag">0</P229>
        <!--Network/Advance/NTP Server-->
        <P30 para="UrlOrIpAddress">{{ ntp_ip|d('pool.ntp.org') }}</P30>
        <P64 para="Preference_TimeZone">{{ XX_timezone_code }}</P64>
        <P143 para="Preference_DHCPTime">0</P143>
        <P75 para="Preference_DaylightSavingTime">{{ XX_timezone_dst }}</P75>
        <!--Setting/Features-->
        {#
        <P53100 para="ForwardAlways_OnOff">0</P53100>
        <P53101 para="ForwardAlways_Target" />
        <P53102 para="ForwardAlways_OnCode" />
        <P53103 para="ForwardAlways_OffCode" />
        <P53110 para="ForwardBusy_OnOff">0</P53110>
        <P53111 para="ForwardBusy_Target" />
        <P53112 para="ForwardBusy_OnCode" />
        <P53113 para="ForwardBusy_OffCode" />
        <P53120 para="ForwardNoAnswer_OnOff">0</P53120>
        <P53124 para="ForwardNoAnswer_AfterRingTime">60</P53124>
        <P53121 para="ForwardNoAnswer_Target" />
        <P53122 para="ForwardNoAnswer_OnCode" />
        <P53123 para="ForwardNoAnswer_OffCode" />
        #}
        {%- if exten_dnd %}
        <P1301 para="DND_WorkType">1</P1301>
        <P53200 para="DND_OnCode">{{ exten_dnd }}</P53200>
        <P53201 para="DND_OffCode">{{ exten_dnd }}</P53201>
        {%- else %}
        <P1301 para="DND_WorkType">0</P1301>
        <P53200 para="DND_OnCode" />
        <P53201 para="DND_OffCode" />
        {%- endif %}

        {%- if XX_fkeys %}
        <!--FunctionKeys/LineKeys-->
        {%- for fnkey, value in XX_fkeys|dictsort(by='key') %}
        <P{{ value['type']['p_nb'] }} para="LineKey{{ fnkey + 1 }}_Type">{{ value['type']['val'] }}</P{{ value['type']['p_nb'] }}>
        <P{{ value['mode']['p_nb'] }} para="LineKey{{ fnkey + 1 }}_Mode">0</P{{ value['mode']['p_nb'] }}>
        <P{{ value['value']['p_nb'] }} para="LineKey{{ fnkey + 1 }}_Value">{{ value['value']['val'] }}</P{{ value['value']['p_nb'] }}>
        <P{{ value['label']['p_nb'] }} para="LineKey{{ fnkey + 1 }}_Label">{{ value['label']['val'] }}</P{{ value['label']['p_nb'] }}>
        <P{{ value['account']['p_nb'] }} para="LineKey{{ fnkey + 1 }}_Account">255</P{{ value['account']['p_nb'] }}>
        <P{{ value['extension']['p_nb'] }} para="LineKey{{ fnkey + 1 }}_Extension">{{ value['extension']['val'] }}</P{{ value['extension']['p_nb'] }}>
        {%- endfor %}
        {%- endif %}
    </config>
</hl_provision>

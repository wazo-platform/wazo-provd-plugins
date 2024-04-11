<?xml version="1.0" encoding="UTF-8"?>
<sysConf>
    <Version>2.0000000000</Version>
    {% if XX_fw_filename -%}
    <fwCheck>
        <EnableAutoUpgrade>1</EnableAutoUpgrade>
        <UpgradeServer1>{{ XX_server_url }}/Fanvil</UpgradeServer1>
        <UpgradeServer2></UpgradeServer2>
        <AutoUpgradeInterval>24</AutoUpgradeInterval>
    </fwCheck>
    {% endif -%}
    <ap>
        <DefaultUsername></DefaultUsername>
        <DefaultPassword></DefaultPassword>
        <InputCfgFileName></InputCfgFileName>
        <DeviceCfgFileKey></DeviceCfgFileKey>
        <CommonCfgFileKey></CommonCfgFileKey>
        <DownloadCommonConf>1</DownloadCommonConf>
        <SaveProvisionInfo>0</SaveProvisionInfo>
        <CheckFailTimes>5</CheckFailTimes>
        <FlashServerIP>{{ XX_server_url }}</FlashServerIP>
        <FlashFileName>Fanvil/$mac.cfg</FlashFileName>
        <FlashProtocol>4</FlashProtocol>
        <FlashMode>1</FlashMode>
        <FlashInterval>1</FlashInterval>
        <updatePBInterval>720</updatePBInterval>
        <pnp>
            <PNPEnable>1</PNPEnable>
            <PNPIP>224.0.1.75</PNPIP>
            <PNPPort>5060</PNPPort>
            <PNPTransport>0</PNPTransport>
            <PNPInterval>1</PNPInterval>
        </pnp>
        <opt>
            <DHCPOption>66</DHCPOption>
            <DhcpOption120>0</DhcpOption120>
            <DHCPv6Option>0</DHCPv6Option>
        </opt>
    </ap>
    <mm>
        <G723BitRate>1</G723BitRate>
        <ILBCPayloadType>97</ILBCPayloadType>
        <ILBCPayloadLen>20</ILBCPayloadLen>
        <AMRPayloadType>108</AMRPayloadType>
        <AMRWBPayloadType>109</AMRWBPayloadType>
        <G726-16PayloadType>103</G726-16PayloadType>
        <G726-24PayloadType>104</G726-24PayloadType>
        <G726-32PayloadType>102</G726-32PayloadType>
        <G726-40PayloadType>105</G726-40PayloadType>
        <DtmfPayloadType>101</DtmfPayloadType>
        <OpusPayloadType>107</OpusPayloadType>
        <OpusSampleRate>0</OpusSampleRate>
        <VAD>0</VAD>
        <H264PayloadType>117</H264PayloadType>
        <H264PacketMode>0</H264PacketMode>
        <H264Profile>0</H264Profile>
        <ResvAudioBand>0</ResvAudioBand>
        <H265PayloadType>98</H265PayloadType>
        <RTPInitialPort>10000</RTPInitialPort>
        <RTPPortQuantity>200</RTPPortQuantity>
        <RTPKeepAlive>0</RTPKeepAlive>
        <RTPRelay>0</RTPRelay>
        <RTCPCNAMEUser></RTCPCNAMEUser>
        <RTCPCNAMEHost></RTCPCNAMEHost>
        <SelectYourTone>25</SelectYourTone>
        <SidetoneGAIN>1</SidetoneGAIN>
        <PlayEgressDTMF>0</PlayEgressDTMF>
        <DialTone>440/0</DialTone>
        <RingbackTone>440/1500,0/3500</RingbackTone>
        <BusyTone>440/500,0/500</BusyTone>
        <CongestionTone>440/500,0/500</CongestionTone>
        <CallwaitingTone>440/300,0/10000</CallwaitingTone>
        <HoldingTone></HoldingTone>
        <ErrorTone></ErrorTone>
        <StutterTone></StutterTone>
        <InformationTone></InformationTone>
        <DialRecallTone></DialRecallTone>
        <MessageTone></MessageTone>
        <HowlerTone></HowlerTone>
        <NumberUnobtainable></NumberUnobtainable>
        <WarningTone></WarningTone>
        <RecordTone></RecordTone>
        <AutoAnswerTone></AutoAnswerTone>
        <capability>
            <AudioCodecSets>G722,PCMU,PCMA</AudioCodecSets>
            <VideoCodecSets>H264</VideoCodecSets>
            <VideoFrameRate>30</VideoFrameRate>
            <VideoBitRate>2000000</VideoBitRate>
            <VideoResolution>7</VideoResolution>
            <VideoNegotiateDir>0</VideoNegotiateDir>
        </capability>
    </mm>
    <phone>
        <MenuPassword>{{ admin_password|d('123') }}</MenuPassword>
        <display>
            <DefaultLanguage>{{ XX_locale }}</DefaultLanguage>
            {% for line_no, line in sip_lines.items() %}
            <LCDTitle>{{ line['display_name']|e }} {{ line['number'] }}</LCDTitle>
            {% endfor %}
        </display>
        <date>
            {% if ntp_enabled -%}
            <SNTPServer>{{ ntp_ip|d('pool.ntp.org') }}</SNTPServer>
            <EnableSNTP>1</EnableSNTP>
            <SNTPTimeout>60</SNTPTimeout>
            {% else -%}
            <EnableSNTP>0</EnableSNTP>
            {% endif -%}
            {% if XX_timezone -%}
            <TimeZone>{{ XX_timezone['time_zone'] }}</TimeZone>
            <TimeZoneName>{{ XX_timezone['time_zone_name'] }}</TimeZoneName>
            {% if XX_timezone['enable_dst'] -%}
            <EnableDST>2</EnableDST>
            <DSTMinOffset>{{ XX_timezone['dst_min_offset'] }}</DSTMinOffset>
            {% macro dst_change(suffix, value) -%}
            <DST{{ suffix }}Mon>{{ value['month'] }}</DST{{ suffix }}Mon>
            <DST{{ suffix }}Hour>{{ value['hour'] }}</DST{{ suffix }}Hour>
            <DST{{ suffix }}Wday>{{ value['dst_wday'] }}</DST{{ suffix }}Wday>
            {% if value['dst_week'] -%}
            <DST{{ suffix }}Week>{{ value['dst_week'] }}</DST{{ suffix }}Week>
            {% endif -%}
            {% endmacro -%}
            {{ dst_change('Start', XX_timezone['dst_start']) }}
            {{ dst_change('End', XX_timezone['dst_end']) }}
            {% else -%}
            <EnableDST>0</EnableDST>
            {% endif -%}
            {%- endif %}
        </date>
        <timeDisplay>
            <EnableTimeDisplay>0</EnableTimeDisplay>
            <TimeDisplayStyle>0</TimeDisplayStyle>
            <DateDisplayStyle>4</DateDisplayStyle>
            <DateSeparator>0</DateSeparator>
        </timeDisplay>
        <softKeyConfig>
            <SoftkeyMode>0</SoftkeyMode>
            <SoftKeyExitStyle>2</SoftKeyExitStyle>
            <DesktopSoftkey>history;contact;dnd;;</DesktopSoftkey>
            <TalkingSoftkey>video;xfer;end;conf;hold;new;mute;record;dialpad;</TalkingSoftkey>
            <RingingSoftkey>forward;audio;video;reject;</RingingSoftkey>
            <AlertingSoftkey>dialpad;xfer;cancel;</AlertingSoftkey>
            <XAlertingSoftkey>dialpad;xfer;cancel;</XAlertingSoftkey>
            <ConferenceSoftkey>conf;dialpad;end;split;hold;mute;exit;</ConferenceSoftkey>
            <WaitingSoftkey>hold;xfer;conf;end;</WaitingSoftkey>
            <EndingSoftkey>complete;autoRedial;end;redial;</EndingSoftkey>
            <DialerPreSoftkey>audio;video;redial;</DialerPreSoftkey>
            <DialerCallSoftkey>audio;video;redial;</DialerCallSoftkey>
            <DialerXferSoftkey>audio;video;xfer;contact;history;cancel;</DialerXferSoftkey>
            <DialerCfwdSoftkey>contact;history;forward;cancel;</DialerCfwdSoftkey>
            <DesktopClick>none;none;none;none;none;</DesktopClick>
            <DailerClick>pline;nline;none;none;none;</DailerClick>
            <RingingClick>none;none;none;none;none;</RingingClick>
            <CallClick>pcall;ncall;voldown;volup;none;</CallClick>
            <DesktopLongPress>status;none;none;mwi;none;</DesktopLongPress>
            <DialerConfSoftkey>audio;video;cancel;contact;history;redial;</DialerConfSoftkey>
        </softKeyConfig>
        {% if XX_xivo_phonebook_url -%}
        <xmlContact index="1">
            <Name>{{ XX_directory|d('Directory') }}</Name>
            <Addr>{{ XX_xivo_phonebook_url }}</Addr>
            <UserName></UserName>
            <PassWd></PassWd>
            <Sipline>-1</Sipline>
            <BindLine>-1</BindLine>
        </xmlContact>
        {%- endif %}
    </phone>
    <cti>
        {% if XX_wazo_phoned_user_service_dnd_enabled_url -%}
        <DNDOnUrl>{{ XX_wazo_phoned_user_service_dnd_enabled_url }}</DNDOnUrl>
        {% endif -%}
        {% if XX_wazo_phoned_user_service_dnd_disabled_url -%}
        <DNDOffUrl>{{ XX_wazo_phoned_user_service_dnd_disabled_url }}</DNDOffUrl>
        {% endif -%}
    </cti>
    <web>
        <WebServerType>0</WebServerType>
        <WebPort>80</WebPort>
        <HttpsWebPort>443</HttpsWebPort>
        <RemoteControl>1</RemoteControl>
        <EnableMMIFilter>0</EnableMMIFilter>
        <WebAuthentication>0</WebAuthentication>
        <EnableTelnet>0</EnableTelnet>
        <TelnetPort>23</TelnetPort>
        <TelnetPrompt></TelnetPrompt>
        <LogonTimeout>15</LogonTimeout>
        {% if admin_password -%}
        <account index="1">
            <Name>admin</Name>
            <Password>{{ admin_password }}</Password>
            <Level>10</Level>
        </account>
        {% endif -%}
        {% if user_password -%}
        <account index="2">
            <Name>guest</Name>
            <Password>{{ user_password }}</Password>
            <Level>5</Level>
        </account>
        {% endif -%}
    </web>
    <qos>
        {% if vlan_enabled -%}
        <EnableVLAN>1</EnableVLAN>
        <VLANID>{{ vlan_id }}</VLANID>
        <SignallingPriority>{{ vlan_priority|d('0') }}</SignallingPriority>
        <VoicePriority>{{ vlan_priority|d('0') }}</VoicePriority>
        {% else -%}
        <Enable_VLAN>0</Enable_VLAN>
        <VLAN_ID>256</VLAN_ID>
        <Signalling_Priority>0</Signalling_Priority>
        <Voice_Priority>0</Voice_Priority>
        {% endif -%}
    </qos>
    <log>
        <OutputDevice>stdout</OutputDevice>
        <FileName>platform.log</FileName>
        <FileSize>512KB</FileSize>
        <SyslogTag>platform</SyslogTag>
        {% if syslog_enabled -%}
        <Level>{{ syslog_level }}</Level>
        <Style>level,tag</Style>
        <SyslogServer>{{ syslog_ip }}</SyslogServer>
        <SyslogServerPort>{{ syslog_port }}</SyslogServerPort>
        {% else -%}
        <Level>ERROR</Level>
        <Style>level,tag</Style>
        <SyslogServer>0.0.0.0</SyslogServer>
        <SyslogServerPort>514</SyslogServerPort>
        {% endif -%}
    </log>
    <sip>
        <SIPPort>5060</SIPPort>
        {% for line_no, line in sip_lines.items() -%}
        <line index="{{ line_no }}">
            {% if line -%}
            <PhoneNumber>{{ line['username']}}</PhoneNumber>
            <DisplayName>{{ line['number'] }} {{ line['display_name']|e }}</DisplayName>
            <RegisterAddr>{{ line['registrar_ip'] }}</RegisterAddr>
            <RegisterPort>{{ line['registrar_port'] }}</RegisterPort>
            <RegisterUser>{{ line['username'] }}</RegisterUser>
            <RegisterPswd>{{ line['password'] }}</RegisterPswd>
            <RegisterTTL>60</RegisterTTL>
            <EnableReg>1</EnableReg>
            <Transport>{{ X_sip_transport_protocol }}</Transport>
            <DTMFMode>{{ line['XX_dtmf_mode'] }}</DTMFMode>
            {% if line['voicemail'] -%}
            <MWINum>{{ line['voicemail'] }}</MWINum>
            {% else -%}
            <MWINum></MWINum>
            {% endif -%}
            <ProxyAddr>{{ line['proxy_ip'] }}</ProxyAddr>
            <ProxyPort>{{ line['proxy_port']|d(5060) }}</ProxyPort>
            <ProxyUser>{{ line['username'] }}</ProxyUser>
            <ProxyPswd>{{ line['password'] }}</ProxyPswd>
            {% if line['backup_proxy_ip'] -%}
            <BackupAddr>{{ line['backup_proxy_ip'] }}</BackupAddr>
            <BackupPort>{{ line['backup_proxy_port'] }}</BackupPort>
            <BackupTransport>{{ X_sip_transport_protocol }}</BackupTransport>
            <BackupTTL>60</BackupTTL>
            <BackupMode>0</BackupMode>
            {% else -%}
            <BackupAddr></BackupAddr>
            <BackupPort></BackupPort>
            <BackupTransport>0</BackupTransport>
            <BackupTTL>3600</BackupTTL>
            <BackupMode>0</BackupMode>
            {% endif -%}
            {% else -%}
            <PhoneNumber></PhoneNumber>
            <DisplayName></DisplayName>
            <RegisterAddr></RegisterAddr>
            <RegisterPort></RegisterPort>
            <RegisterUser></RegisterUser>
            <RegisterPswd></RegisterPswd>
            <EnableReg>0</EnableReg>
            {% endif -%}
        </line>
        {% endfor -%}
    </sip>
    <call>
        <port index="1">
            <AutoOnhook>1</AutoOnhook>
            <AutoOnhookTime>0</AutoOnhookTime>
        </port>
    </call>
    <dsskey>
        {% for page, index, fkey in XX_paginated_fkeys -%}
        {% if loop.index0 == 0 or page != loop.previtem[0] -%}
        <internal index="{{ page }}">
        {%- endif %}
            <Fkey index="{{ index }}">
                <Type>{{ fkey['type'] }}</Type>
                <Value>{{ fkey['value'] }}</Value>
                <Title>{{ fkey['title'] }}</Title>
            </Fkey>
        {%- endfor %}
        </internal>
        {%- else %}
            <Fkey index="2">
                <Type>0</Type>
                <Value></Value>
                <Title></Title>
                <ICON></ICON>
            </Fkey>
            <Fkey index="3">
                <Type>0</Type>
                <Value></Value>
                <Title></Title>
                <ICON></ICON>
            </Fkey>
            <Fkey index="4">
                <Type>0</Type>
                <Value></Value>
                <Title></Title>
                <ICON></ICON>
            </Fkey>
            <Fkey index="5">
                <Type>0</Type>
                <Value></Value>
                <Title></Title>
                <ICON></ICON>
            </Fkey>
            <Fkey index="6">
                <Type>0</Type>
                <Value></Value>
                <Title></Title>
                <ICON></ICON>
            </Fkey>
            <Fkey index="7">
                <Type>0</Type>
                <Value></Value>
                <Title></Title>
                <ICON></ICON>
            </Fkey>
        </internal>
        {% endif -%}

    </dsskey>
</sysConf>

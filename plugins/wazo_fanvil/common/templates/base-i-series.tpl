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
    <sip>
        <SIPPort>5060</SIPPort>
        <STUNServer>stun.wazo.io</STUNServer>
        <STUNPort>443</STUNPort>
        <STUNRefreshTime>50</STUNRefreshTime>
        <SIPWaitStunTime>800</SIPWaitStunTime>
        <ExternNATAddrs></ExternNATAddrs>
        <RegFailInterval>32</RegFailInterval>
        <StrictBranchPrefix>0</StrictBranchPrefix>
        <VideoMuteAttr>0</VideoMuteAttr>
        <EnableGroupBackup>0</EnableGroupBackup>
        <EnableRFC4475>1</EnableRFC4475>
        <StrictUAMatch>0</StrictUAMatch>
        <CSTAEnable>0</CSTAEnable>
        <NotifyReboot>0</NotifyReboot>
        <SMSdirectEnabled>0</SMSdirectEnabled>
        <SMSSaveEnabled>0</SMSSaveEnabled>
        <SMSRingEnabled>0</SMSRingEnabled>
        {% for line_no, line in sip_lines.items() -%}
        <line index="{{ line_no }}">
            {% if line -%}
            <PhoneNumber>{{ line['username']}}</PhoneNumber>
            <DisplayName>{{ line['display_name']|e }}</DisplayName>
            <SipName>WAZO</SipName>
            <RegisterAddr>{{ line['registrar_ip'] }}</RegisterAddr>
            <RegisterPort>{{ line['registrar_port'] }}</RegisterPort>
            <RegisterUser>{{ line['username'] }}</RegisterUser>
            <RegisterPswd>{{ line['password'] }}</RegisterPswd>
            <RegisterTTL>60</RegisterTTL>
            <NeedRegOn>0</NeedRegOn>
            <EnableReg>1</EnableReg>
            <Transport>{{ X_sip_transport_protocol }}</Transport>
            <DTMFMode>{{ line['XX_dtmf_mode'] }}</DTMFMode>
            <ProxyAddr>{{ line['proxy_ip'] }}</ProxyAddr>
            <ProxyPort>{{ line['proxy_port']|d(5060) }}</ProxyPort>
            <ProxyUser>{{ line['username'] }}</ProxyUser>
            <ProxyPswd>{{ line['password'] }}</ProxyPswd>
            <ProxyNeedRegOn>0</ProxyNeedRegOn>
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
            <EnableFailback>1</EnableFailback>
            <FailbackInterval>1800</FailbackInterval>
            <SignalFailback>0</SignalFailback>
            <SignalRetryCounts>3</SignalRetryCounts>
            <SigCryptoKey></SigCryptoKey>
            <EnableOSRTP>0</EnableOSRTP>
            <MediaCrypto>0</MediaCrypto>
            <MedCryptoKey></MedCryptoKey>
            <SRTPAuth-Tag>0</SRTPAuth-Tag>
            <EnableRFC5939>0</EnableRFC5939>
            <LocalDomain></LocalDomain>
            <AlwaysFWD>0</AlwaysFWD>
            <BusyFWD>0</BusyFWD>
            <NoAnswerFWD>0</NoAnswerFWD>
            <AlwaysFWDNum></AlwaysFWDNum>
            <BusyFWDNum></BusyFWDNum>
            <NoAnswerFWDNum></NoAnswerFWDNum>
            <FWDTimer>60</FWDTimer>
            <HotlineNum></HotlineNum>
            <EnableHotline>0</EnableHotline>
            <WarmLineTime>0</WarmLineTime>
            <PickupNum></PickupNum>
            <JoinNum></JoinNum>
            <IntercomNum></IntercomNum>
            <RingType>Default</RingType>
            <NATUDPUpdate>2</NATUDPUpdate>
            <UDPUpdateTTL>30</UDPUpdateTTL>
            <UDPUpdateTryTimes>3</UDPUpdateTryTimes>
            <ServerType>0</ServerType>
            <UserAgent>wazo-fanvil</UserAgent>
            <PRACK>0</PRACK>
            <KeepAUTH>0</KeepAUTH>
            <SessionTimer>1</SessionTimer>
            <STimerExpires>180</STimerExpires>
            <EnableGRUU>0</EnableGRUU>
            <DTMFInfoMode>0</DTMFInfoMode>
            <NATType>1</NATType>
            <EnableRport>1</EnableRport>
            <Subscribe>0</Subscribe>
            <SubExpire>3600</SubExpire>
            <SingleCodec>0</SingleCodec>
            <CLIR>0</CLIR>
            <StrictProxy>1</StrictProxy>
            <DirectContact>0</DirectContact>
            <HistoryInfo>0</HistoryInfo>
            <DNSSRV>0</DNSSRV>
            <DNSMode>0</DNSMode>
            <XFERExpire>0</XFERExpire>
            <BanAnonymous>0</BanAnonymous>
            <DialOffLine>0</DialOffLine>
            <QuotaName>0</QuotaName>
            <PresenceMode>0</PresenceMode>
            <RFCVer>1</RFCVer>
            <PhonePort>0</PhonePort>
            <SignalPort>5060</SignalPort>
            <Transport>0</Transport>
            <UseSRVMixer>0</UseSRVMixer>
            <SRVMixerUri></SRVMixerUri>
            <LongContact>0</LongContact>
            <AutoTCP>0</AutoTCP>
            <UriEscaped>1</UriEscaped>
            <ClicktoTalk>0</ClicktoTalk>
            <MwiNo></MwiNo>
            <MWINum></MWINum>
            <ParkNo></ParkNo>
            <CallParkNum></CallParkNum>
            <RetrieveNum></RetrieveNum>
            <RetrieveType>0</RetrieveType>
            <HelpNo></HelpNo>
            <MSRPHelpNum></MSRPHelpNum>
            <UserIsPhone>1</UserIsPhone>
            <AutoAnswer>0</AutoAnswer>
            <NoAnswerTime>0</NoAnswerTime>
            <MissedCallLog>1</MissedCallLog>
            <ParkMode></ParkMode>
            <SvcCodeMode>0</SvcCodeMode>
            <DNDOnSvcCode></DNDOnSvcCode>
            <DNDOffSvcCode></DNDOffSvcCode>
            <CFUOnSvcCode></CFUOnSvcCode>
            <CFUOffSvcCode></CFUOffSvcCode>
            <CFBOnSvcCode></CFBOnSvcCode>
            <CFBOffSvcCode></CFBOffSvcCode>
            <CFNOnSvcCode></CFNOnSvcCode>
            <CFNOffSvcCode></CFNOffSvcCode>
            <ANCOnSvcCode></ANCOnSvcCode>
            <ANCOffSvcCode></ANCOffSvcCode>
            <SendANOnCode></SendANOnCode>
            <SendANOffCode></SendANOffCode>
            <CWOnCode></CWOnCode>
            <CWOffCode></CWOffCode>
            <VoiceCodecMap></VoiceCodecMap>
            <VideoCodecMap></VideoCodecMap>
            <BLFListUri></BLFListUri>
            <BLFServer></BLFServer>
            <Respond182>0</Respond182>
            <EnableBLFList>0</EnableBLFList>
            <CallerIdType>4</CallerIdType>
            <KeepHigherCallerID>0</KeepHigherCallerID>
            <SynClockTime>0</SynClockTime>
            <MohServer></MohServer>
            <UseVPN>0</UseVPN>
            <EnableDND>0</EnableDND>
            <InactiveHold>0</InactiveHold>
            <ReqWithPort>1</ReqWithPort>
            <UpdateRegExpire>1</UpdateRegExpire>
            <EnableSCA>0</EnableSCA>
            <SubCallPark>0</SubCallPark>
            <SubCCStatus>0</SubCCStatus>
            <FeatureSync>0</FeatureSync>
            <EnableXferBack>0</EnableXferBack>
            <XferBackTime>35</XferBackTime>
            <UseTelCall>0</UseTelCall>
            <EnablePreview>0</EnablePreview>
            <PreviewMode>1</PreviewMode>
            <TLSVersion>2</TLSVersion>
            <CSTANumber></CSTANumber>
            <EnableChgPort>0</EnableChgPort>
            <VQName></VQName>
            <VQServer></VQServer>
            <VQServerPort>5060</VQServerPort>
            <VQHTTPServer></VQHTTPServer>
            <FlashMode>0</FlashMode>
            <ContentType></ContentType>
            <ContentBody></ContentBody>
            <UnregisterOnBoot>0</UnregisterOnBoot>
            <EnableMACHeader>0</EnableMACHeader>
            <EnableRegisterMAC>0</EnableRegisterMAC>
            <RecordStart>Record:on</RecordStart>
            <RecordStop>Record:off</RecordStop>
            <BLFDialogMatch>1</BLFDialogMatch>
            <Ptime>0</Ptime>
            <EnableDeal180>1</EnableDeal180>
            <KeepSingleContact>0</KeepSingleContact>
            <SessionTimerT1>500</SessionTimerT1>
            <SessionTimerT2>4000</SessionTimerT2>
            <SessionTimerT4>5000</SessionTimerT4>
            <UnavailableMode>0</UnavailableMode>
            <TCPUseRetryTimer>0</TCPUseRetryTimer>
            <Call-IDFormat>$id@$ip</Call-IDFormat>
            <GB28181Mode>0</GB28181Mode>
            <ProxyRequire></ProxyRequire>
            <BlockRTPWhenAlerting>0</BlockRTPWhenAlerting>
        </line>
        {% endfor -%}
    </sip>
    <call>
        <port index="1">
            <EnableXferDPlan>0</EnableXferDPlan>
            <EnableFwdDPlan>0</EnableFwdDPlan>
            <EnablePreDPlan>0</EnablePreDPlan>
            <IPDialPrefix>.</IPDialPrefix>
            <EnableDND>1</EnableDND>
            <DNDMode>0</DNDMode>
            <EnableSpaceDND>0</EnableSpaceDND>
            <DNDStartTime>1500</DNDStartTime>
            <DNDEndTime>1730</DNDEndTime>
            <DNDAcceptMcast>0</DNDAcceptMcast>
            <EnableWhiteList>1</EnableWhiteList>
            <EnableBlackList>1</EnableBlackList>
            <EnableCallBar>1</EnableCallBar>
            <MuteRinging>0</MuteRinging>
            <BanDialOut>0</BanDialOut>
            <BanDialOutToneMode>1</BanDialOutToneMode>
            <BanDialOutTone></BanDialOutTone>
            <BanEmptyCID>0</BanEmptyCID>
            <EnableCLIP>1</EnableCLIP>
            <CallWaiting>1</CallWaiting>
            <CallTransfer>0</CallTransfer>
            <CallSemiXfer>0</CallSemiXfer>
            <CallConference>0</CallConference>
            <AutoPickupNext>0</AutoPickupNext>
            <BusyNoLine>1</BusyNoLine>
            <AutoOnhook>1</AutoOnhook>
            <AutoOnhookTime>3</AutoOnhookTime>
            <AutoHangUpTone>1</AutoHangUpTone>
            <EnableIntercom>1</EnableIntercom>
            <IntercomMute>0</IntercomMute>
            <IntercomTone>1</IntercomTone>
            <IntercomBarge>1</IntercomBarge>
            <UseAutoRedial>0</UseAutoRedial>
            <RedialEnterCallLog>0</RedialEnterCallLog>
            <AutoRedialDelay>30</AutoRedialDelay>
            <AutoRedialTimes>5</AutoRedialTimes>
            <CallComplete>0</CallComplete>
            <CHoldingTone>1</CHoldingTone>
            <CWaitingTone>1</CWaitingTone>
            <HideDTMFType>0</HideDTMFType>
            <TalkDTMFTone>1</TalkDTMFTone>
            <DialDTMFTone>1</DialDTMFTone>
            <PswDialMode>0</PswDialMode>
            <PswDialLength>0</PswDialLength>
            <PswDialPrefix></PswDialPrefix>
            <EnableMultiLine>1</EnableMultiLine>
            <AllowIPCall>1</AllowIPCall>
            <CallerNameType>0</CallerNameType>
            <MuteForRing>0</MuteForRing>
            <AutoHandleVideo>1</AutoHandleVideo>
            <DefaultAnsMode>2</DefaultAnsMode>
            <DefaultDialMode>2</DefaultDialMode>
            <HoldToTransfer>0</HoldToTransfer>
            <EnablePreDial>1</EnablePreDial>
            <DefaultExtLine>1</DefaultExtLine>
            <EnableDefLine>1</EnableDefLine>
            <EnableSelLine>1</EnableSelLine>
            <RinginHeadset>0</RinginHeadset>
            <AutoHeadset>0</AutoHeadset>
            <DNDReturnCode>480</DNDReturnCode>
            <BusyReturnCode>486</BusyReturnCode>
            <RejectReturnCode>603</RejectReturnCode>
            <ContactType>0</ContactType>
            <EnableCountryCode>0</EnableCountryCode>
            <CountryCode></CountryCode>
            <CallAreaCode></CallAreaCode>
            <NumberPrivacy>0</NumberPrivacy>
            <PrivacyRule></PrivacyRule>
            <TransfDTMFCode></TransfDTMFCode>
            <HoldDTMFCode></HoldDTMFCode>
            <ConfDTMFCode></ConfDTMFCode>
            <DisableDialSearch>0</DisableDialSearch>
            <CallNumberFilter></CallNumberFilter>
            <AutoResumeCurrent>1</AutoResumeCurrent>
            <CallTimeout>120</CallTimeout>
            <RingTimeout>120</RingTimeout>
            <RingPriority>0</RingPriority>
            <AutoAnswerTone>1</AutoAnswerTone>
            <AlertingTone>1</AlertingTone>
            <BusyTone>1</BusyTone>
            <SnapshotTimeout>60</SnapshotTimeout>
            <DisableSpeakerMode>0</DisableSpeakerMode>
        </port>
    </call>
    <phone>
        <MenuPassword>{{ admin_password|d('123') }}</MenuPassword>
        <KeyLockPassword>{{ admin_password|d('123') }}</KeyLockPassword>
        <display>
            {% for line_no, line in sip_lines.items() %}
            <LCDTitle>{{ line['display_name']|e }} {{ line['number'] }}</LCDTitle>
            {% endfor %}
            <LCDConstrast>5</LCDConstrast>
            <EnableEnergysaving>1</EnableEnergysaving>
            <LCDLuminanceLevel>6</LCDLuminanceLevel>
            <BacklightOffTime>30</BacklightOffTime>
            <DisableCHNIME>0</DisableCHNIME>
            <PhoneModel></PhoneModel>
            <HostName>(none)</HostName>
            <DefaultLanguage>{{ XX_locale }}</DefaultLanguage>
            <EnableGreetings>0</EnableGreetings>
        </display>
        <lineLed>
            <LineIdleColor>0</LineIdleColor>
            <LineIdleCtl>1</LineIdleCtl>
        </lineLed>
        <blfLed>
            <BLFIdleColor>0</BLFIdleColor>
            <BLFIdleCtl>1</BLFIdleCtl>
            <BLFIdleText>terminated</BLFIdleText>
            <BLFRingColor>1</BLFRingColor>
            <BLFRingCtl>2</BLFRingCtl>
            <BLFRingText>early</BLFRingText>
            <BLFDialingColor>1</BLFDialingColor>
            <BLFDialingCtl>0</BLFDialingCtl>
            <BLFDialingText></BLFDialingText>
            <BLFTalkingColor>1</BLFTalkingColor>
            <BLFTalkingCtl>1</BLFTalkingCtl>
            <BLFTalkingText>confirmed</BLFTalkingText>
            <BLFHoldColor>1</BLFHoldColor>
            <BLFHoldCtl>0</BLFHoldCtl>
            <BLFHoldText></BLFHoldText>
            <BLFFailedColor>0</BLFFailedColor>
            <BLFFailedCtl>0</BLFFailedCtl>
            <BLFFailedText>failed</BLFFailedText>
            <BLFParkedColor>0</BLFParkedColor>
            <BLFParkedCtl>3</BLFParkedCtl>
            <BLFParkedText>parked</BLFParkedText>
        </blfLed>
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
            <DateDisplayStyle>9</DateDisplayStyle>
            <DateSeparator>3</DateSeparator>
        </timeDisplay>
{% if XX_wazo_phonebook_url_v2 -%}
       <xmlContact index="1">
            <Name>{{ XX_directory|d('Directory') }}</Name>
            <Addr>{{ XX_wazo_phonebook_url_v2 }}</Addr>
            <UserName></UserName>
            <PassWd></PassWd>
            <Sipline>-1</Sipline>
            <BindLine>-1</BindLine>
            <PhonebookType>0</PhonebookType>
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
        <EnablePVID>0</EnablePVID>
        <PVIDValue>254</PVIDValue>
        <SignallingPriority>{{ vlan_priority|d('0') }}</SignallingPriority>
        <VoicePriority>{{ vlan_priority|d('0') }}</VoicePriority>
        <VideoPriority>{{ vlan_priority|d('0') }}</VideoPriority>
        <LANPortPriority>{{ vlan_priority|d('0') }}</LANPortPriority>
        <EnablediffServ>0</EnablediffServ>
        <SingallingDSCP>46</SingallingDSCP>
        <VoiceDSCP>46</VoiceDSCP>
        <VideoDSCP>46</VideoDSCP>
        <LLDPTransmit>0</LLDPTransmit>
        <LLDPRefreshTime>60</LLDPRefreshTime>
        <LLDPLearnPolicy>0</LLDPLearnPolicy>
        <LLDPSaveLearnData>0</LLDPSaveLearnData>
        <CDPEnable>0</CDPEnable>
        <CDPRefreshTime>60</CDPRefreshTime>
        <DHCPOptionVlan>0</DHCPOptionVlan>
        <DHCPVlanDataType>0</DHCPVlanDataType>
        {% endif -%}
    </qos>

{% block model_specific_fkeys -%}
{% endblock %}

{% block model_specific_parameters -%}
{% endblock %}

    <ap>
        <DownloadCommonConf>1</DownloadCommonConf>
        <SaveProvisionInfo>0</SaveProvisionInfo>
        <CheckFailTimes>1</CheckFailTimes>
        <FlashServerIP>{{ XX_server_url }}</FlashServerIP>
        <FlashFileName>Fanvil/$mac.cfg</FlashFileName>
        <FlashProtocol>4</FlashProtocol>
        <FlashMode>1</FlashMode>
        <FlashInterval>1</FlashInterval>
        <updatePBInterval>720</updatePBInterval>
        <APConfigPriority>0</APConfigPriority>
    </ap>
    <mm>
        <SelectYourTone>{{ XX_country }}</SelectYourTone>
        <capability>
            <AudioCodecSets>PCMU,PCMA,G722</AudioCodecSets>
        </capability>
    </mm>
</sysConf>

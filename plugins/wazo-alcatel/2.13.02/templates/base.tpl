<?xml version="1.0" encoding="UTF-8" ?>
<settings>
{% for line_no, line in sip_lines.items() -%}
    <!-- Account{{ line_no }} Setting -->
    <setting id="Account{{ line_no }}Enable" value="true" />
    <setting id="Account{{ line_no }}RegName" value="{{ line['auth_username']|d(line['username']) }}" />
    <setting id="Account{{ line_no }}Password" value="{{ line['password'] }}" />
    <setting id="Account{{ line_no }}UserName" value="{{ line['auth_username']|d(line['username']) }}" />
    <setting id="Account{{ line_no }}Label" value="{{ line['number'] }} - {{ line['display_name'] }}" />
    <setting id="Account{{ line_no }}DisplayName" value="{{ line['display_name'] }}" />
    <setting id="Account{{ line_no }}Server1Address" value="{{ line['proxy_ip'] }}" />
    <setting id="Account{{ line_no }}Server1Port" value="{{ line['proxy_port'] }}" />
    <setting id="Account{{ line_no }}Server1Transport" value="{{ sip_transport }}" />
    <setting id="Account{{ line_no }}DtmfMode" value="{{ line['XX_user_dtmf_info'] }}" />
    <setting id="Account{{ line_no }}SessionTimer" value="600" />
    <setting id="Account{{ line_no }}SessionTimerRefresher" value="90" />
    <setting id="Account{{ line_no }}UseTlsUriEnable" value="" />
    <setting id="Account{{ line_no }}SrtpWorkingMode" value="0" />
    <setting id="Account{{ line_no }}TlsAnticipationEnable" value="" />
    <setting id="Account{{ line_no }}ServerType" value="0" />
    <setting id="Account{{ line_no }}KeepAliveMode" value="" />
    <setting id="Account{{ line_no }}KeepAliveInterval" value="" />
    <setting id="Account{{ line_no }}Server1Expire" value="600" />
    <setting id="Account{{ line_no }}Server1SubscribleExpire" value="120" />
    {% if line['backup_proxy_ip'] -%}
    <setting id="Account{{ line_no }}Server2Address" value="{{ line['backup_proxy_ip'] }}" />
    <setting id="Account{{ line_no }}Server2Port" value="{{ line['backup_proxy_port'] }}" />
    {% else -%}
    <setting id="Account{{ line_no }}Server2Address" value="" />
    <setting id="Account{{ line_no }}Server2Port" value="5060" />
    {% endif -%}
    <setting id="Account{{ line_no }}Server2Expire" value="600" />
    <setting id="Account{{ line_no }}SwitchoverTimer" value="10" />
    {% if line['outbound_proxy_ip'] -%}
    <setting id="Account{{ line_no }}OutboundProxy1Address" value="{{ line['outbound_proxy_ip'] }}" />
    {% else -%}
    <setting id="Account{{ line_no }}OutboundProxy1Address" value="" />
    {% endif -%}
    {% if line['outbound_proxy_port'] -%}
    <setting id="Account{{ line_no }}OutboundProxy1Port" value="{{ line['outbound_proxy_port'] }}" />
    {% else -%}
    <setting id="Account{{ line_no }}OutboundProxy1Port" value="5060" />
    {% endif -%}
    <!-- Voicemail -->
    <setting id="Account{{ line_no }}VmNumber" value="{{ exten_voicemail }}" />
    <setting id="Account{{ line_no }}MwiUri" value="{{ line['voicemail'] }}" />
    <!-- Rport -->
    <setting id="Account{{ line_no }}RportEnable" value="" />
    <!-- Local Conference -->
    <setting id="Account{{ line_no }}LocalConfEnable" value="" />
    <!-- Voice Codec -->
    <setting id="Account{{ line_no}}AudioCodec" value="0;8;18;9;98;125" />
    <setting id="Account{{ line_no}}OpusBandwidth" value="1" />
    <setting id="Account{{ line_no}}IlbcFrameMode" value="" />
    <!-- Audio SIP -->
    <setting id="Account{{ line_no}}PayloadType" value="" />
    <setting id="Account{{ line_no}}Vad" value="false" />
    <setting id="Account{{ line_no}}Ptime" value="" />
    <!-- Auto Answer -->
    {% if XX_options['switchboard'] -%}
    <setting id="Account{{ line_no }}AutoAnswerEnable" value="true" />
    {% else -%}
    <setting id="Account{{ line_no }}AutoAnswerEnable" value="false" />
    {% endif -%}

    <!-- Intercom -->
    <setting id="Account{{ line_no }}IntercomEnable" value="" />
    <setting id="Account{{ line_no }}IntercomMuteEnable" value="" />
    <setting id="Account{{ line_no }}IntercomToneEnable" value="" />
    <setting id="Account{{ line_no }}IntercomBargeEnable" value="" />
    <setting id="Account{{ line_no }}OutgoingIntercomMethod" value="" />

    <!-- Dailing Rule -->
    <setting id="Account{{ line_no }}DialingRuleInHistoryEnable" value="" />
    <setting id="Account{{ line_no }}DialingRuleInContactEnable" value="" />
    <setting id="Account{{ line_no }}DialingRuleInForwardEnable" value="" />
    <setting id="Account{{ line_no }}DialingRuleInManualEnable" value="" />
    <setting id="Account{{ line_no }}DialingRuleCountryCode" value="" />
    <setting id="Account{{ line_no }}DialingRuleAreaCode" value="" />
    <setting id="Account{{ line_no }}DialingRuleExternalPrefix" value="" />
    <setting id="Account{{ line_no }}DialingRuleMinNumberLength" value="" />
    <setting id="Account{{ line_no }}DialingRuleExternalPrefixExceptions" value="" />

    <setting id="Account{{ line_no }}DigitMap" value="" />
    <setting id="Account{{ line_no }}DigitMapTimer" value="" />
    <setting id="Account{{ line_no }}DigitMapEnable" value="true" />
    <setting id="Account{{ line_no }}DigitMapInHistoryEnable" value="true" />
    <setting id="Account{{ line_no }}DigitMapInDirectoryEnable" value="true" />
    <setting id="Account{{ line_no }}DigitMapInForwardEnable" value="true" />
    <setting id="Account{{ line_no }}DigitMapInManualEnable" value="true" />

    <!-- DND&FWD Sync -->
    <setting id="Account{{ line_no }}DndSyncServerLocalProcessingEnable" value="" />
    <setting id="Account{{ line_no }}DndShareLineSyncServerEnable" value="" />
    <setting id="Account{{ line_no }}FwdSyncServerLocalProcessingEnable" value="" />
{% endfor -%}
    <!-- Provisioning -->
    <setting id="DeviceProvisionServerUrl" value="{{ XX_server_url }}" />
    <setting id="DeviceProvisionServerUsername" value="" />
    <setting id="DeviceProvisionServerPassword" value="" />
    <setting id="DeviceProvisionPollingByWeekdaysEnable" value="" />
    <setting id="DeviceProvisionPollingBeginTime" value="" />
    <setting id="DeviceProvisionPollingEndTime" value="" />
    <setting id="DeviceProvisionPollingDayofWeek" value="" />
    <setting id="DeviceProvisionPollingByIntervalEnable" value="" />

    <!-- Phone Access Permission -->
    <setting id="DeviceUserAccessPermissionEnable" value="" />
    <setting id="DeviceUserAccessPermissionUrl" value="" />
    <setting id="DeviceDefaultAccessLevel" value="" />

{% if user_username -%}
    <setting id="DeviceSecurityUserName" value="{{ user_username|e }}" />
{% else -%}
    <setting id="DeviceSecurityUserName" value="user" />
{% endif -%}
{% if user_password -%}
    <setting id="DeviceSecurityUserPwd" value="{{ user_password|e }}" />
    <setting id="DeviceSecurityVarPwd" value="{{ user_password|e }}" />
{% else -%}
    <setting id="DeviceSecurityUserPwd" value="user" />
    <setting id="DeviceSecurityVarPwd" value="var" />
{% endif -%}
    <setting id="DeviceSecurityVarName " value="var" />
{% if admin_username -%}
    <setting id="DeviceSecurityAdminName" value="{{ admin_username|e }}" />
{% else -%}
    <setting id="DeviceSecurityAdminName" value="admin" />
{% endif -%}
{% if admin_password -%}
    <setting id="DeviceSecurityAdminPwd" value="{{ admin_password|e }}" />
{% else -%}
    <setting id="DeviceSecurityAdminPwd" value="123456" />
{% endif -%}
    <setting id="DeviceSecuritySshEnable" value="false" />

    <!-- Provision file -->
    <setting id="DeviceProvisionFileFirst" value="config.$model.xml" />
    <setting id="DeviceProvisionFileSecond" value="config.$mac.xml" />
    <setting id="DeviceProvisionFileThird" value="" />
    <setting id="DeviceNetworkConnectExpiredTime" value="10" />
    <setting id="DeviceProvisionAttemptExpiredTime" value="20" />
    <setting id="DeviceProvisionImmediateUpdateTimes" value="" />

    <setting id="SIPMaxCall" value="" />
    <setting id="SIPConfPartyMax" value="" />

    <!-- Mtu -->
    <setting id="DeviceNetworkMtu" value="" />

    <!-- ringing Timeout -->
    <setting id="SettingRingingTimeout" value="" />
    <setting id="FeatureAutoDialOutTimer " value="" />

    <!-- Tone Settings -->
    <setting id="SettingCountryTone" value="" />
    <setting id="FeatureDialingToneEnable" value="" />
    <setting id="SettingDtmfFeedbackEnable" value="" />
    <setting id="SettingDtmfDuration" value="" />

    <!-- DNS -->
{% if dns_enabled -%}
    <setting id="DeviceNetworkDns1" value="{{ dns_ip }}" />
{% else -%}
    <setting id="DeviceNetworkDns1" value="" />
{% endif -%}
    <setting id="DeviceNetworkDns2" value="" />

    <!-- VLAN Settings -->
{% if vlan_enabled -%}
    <setting id="DeviceNetworkLanVlanEnable" value="true" />
    <setting id="DeviceNetworkLanVlanNumber" value="{{ vlan_id }}" />
    {% if vlan_pc_port_id -%}
    <setting id="DeviceNetworkPcVlanEnable" value="true" />
    <setting id="DeviceNetworkPcVlanNumber" value="{{ vlan_pc_port_id }}" />
    {% else -%}
    <setting id="DeviceNetworkPcVlanEnable" value="false" />
    <setting id="DeviceNetworkPcVlanNumber" value="" />
    {% endif -%}
{% else -%}
    <setting id="DeviceNetworkLanVlanEnable" value="false" />
    <setting id="DeviceNetworkLanVlanNumber" value="" />
    <setting id="DeviceNetworkPcVlanEnable" value="false" />
    <setting id="DeviceNetworkPcVlanNumber" value="" />
{% endif -%}
    <setting id="DeviceNetworkLldpVlanEnable" value="" />
    <setting id="DeviceNetworkPcVlanFilterEnable" value="" />

    <!-- Timezone Setting -->
    <setting id="SettingTimeZone" value="{{ XX_timezone }}" />
    <setting id="SettingTimeZoneLocation" value="{{ timezone }}" />
    <setting id="SettingDstEnable" value="2" />
    {% if ntp_enabled -%}
    <setting id="SettingSntpServer" value="{{ ntp_ip }}" />
    {% else -%}
    <setting id="SettingSntpServer" value="" />
    {% endif -%}
    <setting id="SettingSntpRefreshPeriod" value="" />

    <!-- Date Time Format -->
    <setting id="SettingDateFormat" value="" />
    <setting id="SettingTimeFormat" value="" />

    <!-- Language Setting -->
    <setting id="SettingLanguage" value="{{ XX_lang }}" />
    <setting id="SettingWuiLanguage" value="" />

    <!-- Firmware Upgrading -->
    <setting id="DeviceFirmwareUpgradeUrl" value="{{ XX_server_url }}/firmware" />
    <setting id="DeviceAutoUpgradeEnable" value="true" />
    <setting id="DeviceAutoUpgradeCheckTime" value="" />
    <setting id="DeviceAutoUpgradeTimeRandom" value="" />

    <!-- peer to peer -->
    <setting id="SIPIpCallEnable" value="" />
    <setting id="SIPPeerFilterEnable" value="" />

    <!-- Audio HearingAid -->
    <setting id="AudioHearingAidEnable" value="false" />

    <!-- Forward Setting -->
    <setting id="FeatureFwdMode" value="" />
    <setting id="FeatureFwdMethod" value="" />
    <setting id="FeatureImmFwdEnable" value="" />
    <setting id="FeatureImmFwdNumber" value="" />
    <setting id="FeatureImmFwdOnCode" value="" />
    <setting id="FeatureImmFwdOffCode" value="" />
    <setting id="FeatureBusyFwdEnable" value="" />
    <setting id="FeatureBusyFwdNumber" value="" />
    <setting id="FeatureBusyFwdOnCode" value="" />
    <setting id="FeatureBusyFwdOffCode" value="" />
    <setting id="FeatureNoReplyFwdEnable" value="" />
    <setting id="FeatureNoReplyFwdNumber" value="" />
    <setting id="FeatureNoReplyFwdOnCode" value="" />
    <setting id="FeatureNoReplyFwdOffCode" value="" />

    <!-- DND Setting -->
    <setting id="FeatureDndMode" value="" />
    <setting id="FeatureDNDMethod" value="" />
    <setting id="FeatureDndEnable" value="" />
    <setting id="FeatureDndOnCode" value="" />
    <setting id="FeatureDndOffCode" value="" />

    <!-- DTMF -->
    <setting id="FeatureDtmfHideEnable" value="" />
    <setting id="FeatureDtmfHideDelay" value="" />

    <!-- Redialkey Setting -->
    <setting id="FeatureRedialKeyMode" value="" />

    <!-- Keep Mute -->
    <setting id="FeatureKeepMuteEnable" value="" />

    <!-- Auto Redial -->
    <setting id="FeatureAutoRedialEnable" value="" />
    <setting id="FeatureAutoRedialTimes" value="" />
    <setting id="FeatureAutoRedialInterval" value="" />

    <!-- Directory Search Rules -->
    <setting id="SettingDirectorySearchType" value="" />

    <!-- USB Recording -->
    <setting id="FeatureUsbCallRecordingEnable" value="" />
    <setting id="FeatureAutoRecordingEnable" value="" />

    <!-- Wallpaper  -->
    <setting id="SettingWallpaperUploadUrl" value="" />
    <setting id="SettingWallpaperDelete" value="" />
    <setting id="SettingWallpaperDisplay" value="" />

    <!-- Local Phonebook -->
    <setting id="LocalContactUploadUrl" value="" />

    <!-- Remote Phonebook -->
    <setting id="RemotePhoneBookEnable" value="" />
    <setting id="RemotePhoneBookForceUpdateMode" value="" />
    <setting id="RemotePhoneBookPeriodUpdateEnable" value="" />
    <setting id="RemotePhoneBookPeriodUpdateInterval" value="" />

    <!-- Remote Phonebook Group-->
    <setting id="RemotePhoneBook1GroupName" value="" />
    <setting id="RemotePhoneBook1Url" value="" />
    <setting id="RemotePhoneBook1AuthName" value="" />
    <setting id="RemotePhoneBook1AuthPwd" value="" />

    <setting id="RemotePhoneBook2GroupName" value="" />
    <setting id="RemotePhoneBook2Url" value="" />
    <setting id="RemotePhoneBook2AuthName" value="" />
    <setting id="RemotePhoneBook2AuthPwd" value="" />

    <setting id="RemotePhoneBook3GroupName" value="" />
    <setting id="RemotePhoneBook3Url" value="" />
    <setting id="RemotePhoneBook3AuthName" value="" />
    <setting id="RemotePhoneBook3AuthPwd" value="" />

    <setting id="RemotePhoneBook4GroupName" value="" />
    <setting id="RemotePhoneBook4Url" value="" />
    <setting id="RemotePhoneBook4AuthName" value="" />
    <setting id="RemotePhoneBook4AuthPwd" value="" />

    <setting id="RemotePhoneBook5GroupName" value="" />
    <setting id="RemotePhoneBook5Url" value="" />
    <setting id="RemotePhoneBook5AuthName" value="" />
    <setting id="RemotePhoneBook5AuthPwd" value="" />

    <setting id="RemotePhoneBook6GroupName" value="" />
    <setting id="RemotePhoneBook6Url" value="" />
    <setting id="RemotePhoneBook6AuthName" value="" />
    <setting id="RemotePhoneBook6AuthPwd" value="" />


    <!-- Callog Contact backup-->
    <setting id="DeviceBackupUploadDelayTime" value="" />
    <setting id="DeviceBackupUploadMethod" value="" />
    <setting id="DeviceBackupUploadTime" value="" />
    <setting id="DeviceBackupUrl" value="" override="" />
    <setting id="DeviceCallLogBackupEnable" value="" />
    <setting id="DeviceContactBackupEnable" value="" />

    <!-- Config file encryption -->
    <setting id="DeviceSecurityEncryptionAesKey" value="" />


    <!-- Call completion -->
    <setting id="FeatureCallCompletionEnable" value="" />

    <!-- Call Display-->
    <setting id="SettingCallInfoDisplayMode" value="" />
    <setting id="SettingCallInfoDisplaySource" value="" />


    <!-- Call Number Filter-->
    <setting id="FeatureCallNumberFilter" value="" />

    <!-- Call Hold Method-->
    <setting id="SIPRfc2543HoldEnable" value="" />
    <setting id="FeatureHoldUseInactiveEnable" value="" />

    <!-- Notification popup -->
    <setting id="FeatureVmPopupEnable" value="" />

    <!-- Password dialing -->
    <setting id="FeatureConfidentialDialEnable" value="" />
    <setting id="FeatureConfidentialDialPrefix" value="" />
    <setting id="FeatureConfidentialDialLength" value="" />

    <!-- Span to PC -->
    <setting id="DeviceNetworkSpanToPcType" value="" />

    <!--  Favorite Contacts -->
    <setting id="DirectoryFavoriteMode" value="0" />

    <!-- Search source list -->
    <setting id="DirectorySearchInDialingList" value="0;1" />

    <!-- Directory List -->
    <setting id="DirectoryList" value="0" />

    <!-- Softkey Layout -->
    <setting id="SettingCustomSoftkeyEnable" value="false" />
    <setting id="SettingCustomSoftkeyStateList" value="" />
    <setting id="SettingCustomSoftkeyDynamicEnable" value="true" />
    <setting id="SettingCustomSoftkeyDialUrl" value="" />
    <setting id="SettingCustomSoftkeyCallOutUrl" value="" />
    <setting id="SettingCustomSoftkeyCallFailedUrl" value="" />
    <setting id="SettingCustomSoftkeyCallInUrl" value="" />
    <setting id="SettingCustomSoftkeyTalkingUrl" value="" />

    <setting id="SettingCustomSoftkeyDial" value="" />
    <setting id="SettingCustomSoftkeyDialEmpty" value="" />
    <setting id="SettingCustomSoftkeyTransDial" value="" />
    <setting id="SettingCustomSoftkeyTransDialEmpty" value="" />
    <setting id="SettingCustomSoftkeyConfDial" value="" />
    <setting id="SettingCustomSoftkeyConfDialEmpty" value="" />
    <setting id="SettingCustomSoftkeyCalling" value="" />
    <setting id="SettingCustomSoftkeyTransferring" value="" />
    <setting id="SettingCustomSoftkeyCallFailed" value="" />
    <setting id="SettingCustomSoftkeyRinging" value="" />
    <setting id="SettingCustomSoftkeyNewCallin" value="" />
    <setting id="SettingCustomSoftkeyConfNewCallin" value="" />
    <setting id="SettingCustomSoftkeyConversation" value="" />
    <setting id="SettingCustomSoftkeyHold" value="" />
    <setting id="SettingCustomSoftkeyHeld" value="" />
    <setting id="SettingCustomSoftkeyConf" value="" />
    <setting id="SettingCustomSoftkeyConfHold" value="" />
    <setting id="SettingCustomSoftkeyBeTrans" value="" />
    <setting id="SettingCustomSoftkeyPaging" value="" />
    <setting id="SettingCustomSoftkeyListening" value="" />

    <!-- WBM HTTP/HTTPS -->
    <setting id="DeviceNetworkHttpEnable" value="true" />
    <setting id="DeviceNetworkHttpPort" value="80" />
    <setting id="DeviceNetworkHttpsEnable" value="true" />
    <setting id="DeviceNetworkHttpsPort" value="443" />
    <setting id="DeviceNetworkHttpsDefaultEnable" value="true" />

    <!-- Hold tone -->
    <setting id="FeaturePlayHoldToneEnable" value="true" />
    <setting id="FeaturePlayHoldToneDelay" value="30" />
    <setting id="FeaturePlayHoldToneInterval" value="30" />
    <setting id="FeaturePlayHeldToneEnable" value="false" />
    <setting id="FeaturePlayHeldToneDelay" value="30" />
    <setting id="FeaturePlayHeldToneInterval" value="30" />

    <!-- Call Waiting Sync-->
    <setting id="FeatureCallWaitingEnable" value="true" />
    <setting id="FeatureCallWaitingToneEnable" value="true" />
    <setting id="FeatureCallWaitingOnCode" value="" />
    <setting id="FeatureCallWaitingOffCode" value="" />

    <!-- PNP DHCP -->
    <setting id="DeviceProvisionPnpEnable" value="true" />
    <setting id="DeviceProvisionDhcpEnable" value="true" />
    <setting id="DeviceProvisionDhcpCustomOption" value="" />
    <setting id="DeviceProvisionDhcpCustomOptionIpv6" value="" />

    <!-- User Configuration Protection -->
    <setting id="DeviceProvisionUserConfigProtectEnable" value="false" />
    <setting id="DeviceProvisionUserConfigSyncEnable" value="false" />
    <setting id="DeviceProvisionUserConfigSyncPath" value="" />
    <setting id="DeviceProvisionUserConfigUploadMethod" value="1" />

    <!-- Digit Map -->
    <setting id="DigitMapEnable" value="" />
    <setting id="DigitMap" value="[2-9]11;0T;+011xxx.T;0[2-9]xxxxxxxxx;+1[2-9]xxxxxxxx;[2-9]xxxxxxxxx;[2-9]xxxT" />
    <setting id="DigitMapTimer" value="3" />
    <setting id="DigitMapInHistoryEnable" value="true" />
    <setting id="DigitMapInDirectoryEnable" value="true" />
    <setting id="DigitMapInForwardEnable" value="true" />
    <setting id="DigitMapInManualEnable" value="true" />

    <!-- Log level -->
    <setting id="DeviceLogLevel" value="1" />

    <!-- Programm Key -->
{% for fkey in XX_fkeys -%}
    <setting id="ProgramKey{{ fkey['position'] }}Type" value="{{ fkey['type'] }}" />
    <setting id="ProgramKey{{ fkey['position'] }}Account" value="1" />
    <setting id="ProgramKey{{ fkey['position'] }}Label" value="{{ fkey['label']|e }}" />
    <setting id="ProgramKey{{ fkey['position'] }}Value" value="{{ fkey['value'] }}" />
    <setting id="ProgramKey{{ fkey['position'] }}Extension" value="{{ fkey['extension'] }}" />
{% endfor -%}

    <!-- Programm AOM 1-2-3 key -->
    <!-- AOM1-->
    <setting id="Aom1ProgramKey1Type" value="" />
    <setting id="Aom1ProgramKey1Account" value="" />
    <setting id="Aom1ProgramKey1Label" value="" />
    <setting id="Aom1ProgramKey1Value" value="" />
    <setting id="Aom1ProgramKey1Extension" value="" />
    <setting id="Aom1ProgramKey2Type" value="" />
    <setting id="Aom1ProgramKey2Account" value="" />
    <setting id="Aom1ProgramKey2Label" value="" />
    <setting id="Aom1ProgramKey2Number" value="" />
    <setting id="Aom1ProgramKeyy2Extension" value="" />

    <!-- AOM2-->
    <setting id="Aom2ProgramKey1Type" value="" />
    <setting id="Aom2ProgramKey1Account" value="" />
    <setting id="Aom2ProgramKey1Label" value="" />
    <setting id="Aom2ProgramKey1Number" value="" />
    <setting id="Aom2ProgramKey1Extension" value="" />
    <setting id="Aom2ProgramKey2Type" value="" />
    <setting id="Aom2ProgramKey2Account" value="" />
    <setting id="Aom2ProgramKey2Label" value="" />
    <setting id="Aom2ProgramKey2Number" value="" />
    <setting id="Aom2ProgramKey2Extension" value="" />

    <!-- AOM3-->
    <setting id="Aom3ProgramKey1Type" value="" />
    <setting id="Aom3ProgramKey1Account" value="" />
    <setting id="Aom3ProgramKey1Label" value="" />
    <setting id="Aom3ProgramKey1Number" value="" />
    <setting id="Aom3ProgramKey1Extension" value="" />
    <setting id="Aom3ProgramKey2Type" value="" />
    <setting id="Aom3ProgramKey2Account" value="" />
    <setting id="Aom3ProgramKey2Label" value="" />
    <setting id="Aom3ProgramKey2Number" value="" />
    <setting id="Aom3ProgramKey2Extension" value="" />

    <!-- DesktopDynamicKey 1 -->
    <setting id="DynamicSoftKey1Type" value="" />
    <setting id="DynamicSoftKey1Account" value="" />
    <setting id="DynamicSoftKey1Label" value="" />
    <setting id="DynamicSoftKey1Value" value="" />
    <setting id="DynamicSoftKey1Extension" value="" />

    <!-- DesktopDynamicKey 2 -->
    <setting id="DynamicSoftKey2Type" value="" />
    <setting id="DynamicSoftKey2Account" value="" />
    <setting id="DynamicSoftKey2Label" value="" />
    <setting id="DynamicSoftKey2Value" value="" />
    <setting id="DynamicSoftKey2Extension" value="" />

    <!-- DesktopDynamicKey 3 -->
    <setting id="DynamicSoftKey3Type" value="" />
    <setting id="DynamicSoftKey3Account" value="" />
    <setting id="DynamicSoftKey3Label" value="" />
    <setting id="DynamicSoftKey3Value" value="" />
    <setting id="DynamicSoftKey3Extension" value="" />

    <!-- DesktopDynamicKey 4 -->
    <setting id="DynamicSoftKey4Type" value="" />
    <setting id="DynamicSoftKey4Account" value="" />
    <setting id="DynamicSoftKey4Label" value="" />
    <setting id="DynamicSoftKey4Value" value="" />
    <setting id="DynamicSoftKey4Extension" value="" />

</settings>

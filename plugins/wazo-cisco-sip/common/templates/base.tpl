<device>
  <deviceProtocol>SIP</deviceProtocol>
  <sshUserId>admin</sshUserId>
  <sshPassword>{{ admin_password }}</sshPassword>
  <devicePool>
    <dateTimeSetting>
      <dateTemplate>D-M-YA</dateTemplate>
      <timeZone>{{ XX_timezone }}</timeZone>
      <ntps>
        {% if ntp_enabled -%}
        <ntp>
          <name>{{ ntp_ip }}</name>
          <ntpMode>Unicast</ntpMode>
        </ntp>
        {% endif -%}
      </ntps>
    </dateTimeSetting>
    <callManagerGroup>
      <members>
        <member priority="0">
          <callManager>
            <ports>
              <ethernetPhonePort>2000</ethernetPhonePort>
              <sipPort>{{ sip_proxy_port }}</sipPort>
              <securedSipPort>5061</securedSipPort>
            </ports>
            <processNodeName>{{ sip_proxy_ip }}</processNodeName>
          </callManager>
        </member>
      </members>
    </callManagerGroup>
  </devicePool>
  <sipProfile>
    <sipProxies>
      <backupProxy>{{ sip_backup_proxy_ip }}</backupProxy>
      <backupProxyPort>{{ sip_backup_proxy_port }}</backupProxyPort>
      <emergencyProxy></emergencyProxy>
      <emergencyProxyPort></emergencyProxyPort>
      <outboundProxy>{{ sip_outbound_proxy_ip }}</outboundProxy>
      <outboundProxyPort>{{ sip_outbound_proxy_port }}</outboundProxyPort>
      <registerWithProxy>true</registerWithProxy>
    </sipProxies>
    <sipCallFeatures>
      <cnfJoinEnabled>true</cnfJoinEnabled>
      <callForwardURI>x-serviceuri-cfwdall</callForwardURI>
      <callPickupURI>x-cisco-serviceuri-pickup</callPickupURI>
      <callPickupListURI>x-cisco-serviceuri-opickup</callPickupListURI>
      <callPickupGroupURI>x-cisco-serviceuri-gpickup</callPickupGroupURI>
      <meetMeServiceURI>x-cisco-serviceuri-meetme</meetMeServiceURI>
      <abbreviatedDialURI>x-cisco-serviceuri-abbrdial</abbreviatedDialURI>
      <rfc2543Hold>false</rfc2543Hold>
      <callHoldRingback>2</callHoldRingback>
      <localCfwdEnable>true</localCfwdEnable>
      <semiAttendedTransfer>true</semiAttendedTransfer>
      <anonymousCallBlock>2</anonymousCallBlock>
      <callerIdBlocking>2</callerIdBlocking>
      <dndControl>0</dndControl>
      <remoteCcEnable>true</remoteCcEnable>
    </sipCallFeatures>
    <sipStack>
      <sipInviteRetx>6</sipInviteRetx>
      <sipRetx>10</sipRetx>
      <timerInviteExpires>180</timerInviteExpires>
      <timerRegisterExpires>3600</timerRegisterExpires>
      <timerRegisterDelta>5</timerRegisterDelta>
      <timerKeepAliveExpires>120</timerKeepAliveExpires>
      <timerSubscribeExpires>120</timerSubscribeExpires>
      <timerSubscribeDelta>5</timerSubscribeDelta>
      <timerT1>500</timerT1>
      <timerT2>4000</timerT2>
      <maxRedirects>70</maxRedirects>
      <remotePartyID>false</remotePartyID>
      <userInfo>None</userInfo>
    </sipStack>
    <autoAnswerTimer>1</autoAnswerTimer>
    <autoAnswerAltBehavior>false</autoAnswerAltBehavior>
    <autoAnswerOverride>true</autoAnswerOverride>
    <transferOnhookEnabled>false</transferOnhookEnabled>
    <enableVad>false</enableVad>
    <dtmfAvtPayload>101</dtmfAvtPayload>
    <dtmfDbLevel>3</dtmfDbLevel>
    <dtmfOutofBand>avt</dtmfOutofBand>
    <alwaysUsePrimeLine>false</alwaysUsePrimeLine>
    <alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
    <kpml>3</kpml>
    <phoneLabel></phoneLabel>
    <stutterMsgWaiting>1</stutterMsgWaiting>
    <callStats>false</callStats>
    <silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
    <disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
    <sipLines>
    {% for line_no, line in sip_lines.iteritems() %}
      <line button="{{ line_no }}" lineIndex="{{ line_no }}">
        <featureID>9</featureID>
        <featureLabel>{{ line['number'] }}</featureLabel>
        <proxy>USECALLMANAGER</proxy>
        <port>{{ line['proxy_port']|d(5060) }}</port>
        <name>{{ line['username'] }}</name>
        <displayName>{{ line['display_name'] }}</displayName>
        <autoAnswer>
          <autoAnswerEnabled>2</autoAnswerEnabled>
        </autoAnswer>
        <callWaiting>3</callWaiting>
        <authName>{{ line['auth_username'] }}</authName>
        <authPassword>{{ line['password'] }}</authPassword>
        <sharedLine>false</sharedLine>
        <messageWaitingLampPolicy>1</messageWaitingLampPolicy>
        {% if line['voicemail'] -%}
        <messagesNumber>{{ line['voicemail'] }}</messagesNumber>
        {% endif -%}
        <ringSettingIdle>4</ringSettingIdle>
        <ringSettingActive>5</ringSettingActive>
        <contact>{{ line['number'] }}</contact>
        <forwardCallInfoDisplay>
          <callerName>true</callerName>
          <callerNumber>false</callerNumber>
          <redirectedNumber>false</redirectedNumber>
          <dialedNumber>true</dialedNumber>
        </forwardCallInfoDisplay>
      </line>
    {% endfor -%}
    </sipLines>
    <voipControlPort>{{ sip_registrar_port }}</voipControlPort>
    <startMediaPort>16348</startMediaPort>
    <stopMediaPort>20134</stopMediaPort>
    <dscpForAudio>184</dscpForAudio>
    <ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
    <dialTemplate>dialplan.xml</dialTemplate>
    <softKeyFile></softKeyFile>
  </sipProfile>
  <commonProfile>
    {% if admin_password -%}
    <phonePassword>{{ admin_password }}</phonePassword>
    {% endif -%}
    <backgroundImageAccess>true</backgroundImageAccess>
    <callLogBlfEnabled>2</callLogBlfEnabled>
  </commonProfile>
  <loadInformation>{% block loadInformation %}{% endblock %}</loadInformation>
  <vendorConfig>
    <disableSpeaker>false</disableSpeaker>
    <disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
    <pcPort>0</pcPort>
    <settingsAccess>1</settingsAccess>
    <garp>0</garp>
    {% if vlan_enabled -%}
    <voiceVlanAccess>{{ vlan_id }}</voiceVlanAccess>
    {% endif -%}
    <videoCapability>1</videoCapability>
    <autoSelectLineEnable>0</autoSelectLineEnable>
    <webAccess>1</webAccess>
    <daysDisplayNotActive>1,2,3,4,5,6,7</daysDisplayNotActive>
    <displayOnTime>00:00</displayOnTime>
    <displayOnDuration>00:00</displayOnDuration>
    <displayIdleTimeout>00:00</displayIdleTimeout>
    <spanToPCPort>1</spanToPCPort>
    <loggingDisplay>1</loggingDisplay>
    <loadServer></loadServer>
  </vendorConfig>
  {% if XX_locale -%}
  <userLocale>
    <name>i18n/{{ XX_locale[0] }}</name>
    <langCode>{{ XX_locale[1] }}</langCode>
  </userLocale>
  <networkLocale>i18n/{{ XX_locale[2] }}</networkLocale>
  {% endif -%}
  <networkLocaleInfo>
    <name></name>
    <uid></uid>
    <version>1.0.0.0-1</version>
  </networkLocaleInfo>
  <deviceSecurityMode>1</deviceSecurityMode>
  <authenticationURL></authenticationURL>
  <directoryURL>{{ XX_xivo_phonebook_url|e }}</directoryURL>
  <servicesURL></servicesURL>
  <idleURL></idleURL>
  <informationURL></informationURL>
  <messagesURL></messagesURL>
  <proxyServerURL></proxyServerURL>
  <dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
  <dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
  <dscpForCm2Dvce>96</dscpForCm2Dvce>
  <transportLayerProtocol>2</transportLayerProtocol>
  <capfAuthMode>0</capfAuthMode>
  <capfList>
    <capf>
      <phonePort>3804</phonePort>
    </capf>
  </capfList>
  <certHash></certHash>
  <encrConfig>false</encrConfig>
  <addOnModules>{{ XX_addons }}</addOnModules>
</device>

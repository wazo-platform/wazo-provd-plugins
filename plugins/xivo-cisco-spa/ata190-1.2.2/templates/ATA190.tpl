<?xml version="1.0"?>
<device>
	<deviceProtocol>SIP</deviceProtocol>
	<devicePool>
		<dateTimeSetting>
			<dateTemplate>YA.M.D</dateTemplate>
        {% if timezone %}
			<timeZone>{{ timezone }}</timeZone>
        {% endif %}
			<olsonTimeZone>America/Toronto</olsonTimeZone>
            {% if ntp_enabled %}
			<ntps>
				<ntp>
					<name>{{ ntp_ip }}</name>
					<ntpMode>Unicast</ntpMode>
				</ntp>
			</ntps>
            {% endif %}
		</dateTimeSetting>
		<callManagerGroup>
			<name>Default</name>
			<tftpDefault>true</tftpDefault>
			<members>
				<member>
				</member>
			</members>
		</callManagerGroup>
		<srstInfo>
			<userModifiable>false</userModifiable>
			<isSecure>false</isSecure>
		</srstInfo>
	</devicePool>
	<sipProfile>
	{% set line_nb = '1' %}
	{% if XX_second_line_ata and '2' in sip_lines %}
	{% set line_nb = '2' %}
	{% endif %}

		<phoneLabel>{{ sip_lines[line_nb]['number'] }}</phoneLabel>
	
		<sipCallFeatures>
			<cnfJoinEnabled>true</cnfJoinEnabled>
			<rfc2543Hold>false</rfc2543Hold>
			<callHoldRingback>2</callHoldRingback>
			<localCfwdEnable>true</localCfwdEnable>
			<semiAttendedTransfer>true</semiAttendedTransfer>
			<anonymousCallBlock>2</anonymousCallBlock>
			<callerIdBlocking>2</callerIdBlocking>
			<dndControl>0</dndControl>
			<remoteCcEnable>true</remoteCcEnable>
			<retainForwardInformation>true</retainForwardInformation>

            <callForwardURI>x-cisco-serviceuri-cfwdall</callForwardURI>
            <callPickupURI>x-cisco-serviceuri-pickup</callPickupURI>
            <callPickupListURI>x-cisco-serviceuri-opickup</callPickupListURI>
            <callPickupGroupURI>x-cisco-serviceuri-gpickup</callPickupGroupURI>
            <meetMeServiceURI>x-cisco-serviceuri-meetme</meetMeServiceURI>
            <abbreviatedDialURI>x-cisco-serviceuri-abbrdial</abbreviatedDialURI>
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
			<remotePartyID>true</remotePartyID>
			<userInfo>Phone</userInfo>
		</sipStack>
		<sipLines>
            {% set line = sip_lines[line_nb] %}
			<line>
				<featureID>9</featureID>
				<featureLabel>{{ line['display_name'] }}</featureLabel>
				<proxy>{{ line['proxy_ip'] }}</proxy>
				<port>{{ line['proxy_port']|d(5060) }}</port>
				<displayName>{{ line['number'] }}</displayName>
				<contact>{{ line['number'] }}</contact>
				<name>{{ line['username'] }}</name>
				<authName>{{ line['auth_username'] }}</authName>
				<authPassword>{{ line['password'] }}</authPassword>
				<sharedLine>false</sharedLine>
			</line>
		</sipLines>
		<dialTemplate>dialplan.xml</dialTemplate>
		
	</sipProfile>
	{% if XX_locale -%}
        <userLocale>
            <name>i18n/{{ XX_locale[0] }}</name>
            <langCode>{{ XX_locale[1] }}</langCode>
        </userLocale>
        <networkLocale>i18n/{{ XX_locale[2] }}</networkLocale>
    {% endif -%}
</device>

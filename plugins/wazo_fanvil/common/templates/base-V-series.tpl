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
            <RingPriority>0</RingPriority>
        </port>
    </call>
    <phone>
        <MenuPassword>{{ admin_password|d('123') }}</MenuPassword>
        <KeyLockPassword>123</KeyLockPassword>
        <FastKeylockCode></FastKeylockCode>
        <EnableKeyLock>0</EnableKeyLock>
        <KeyLockTimeout>0</KeyLockTimeout>
        <KeyLockStatus>0</KeyLockStatus>
        <EmergencyCall>112</EmergencyCall>
        <PushXMLIP></PushXMLIP>
        <SIPNumberPlan>0</SIPNumberPlan>
        <LDAPSearch>0</LDAPSearch>
        <SearchPath>0</SearchPath>
        <CallerDisplayType>5</CallerDisplayType>
        <CallLogDisplayType>0</CallLogDisplayType>
        <EnableRecvSMS>1</EnableRecvSMS>
        <EnableCallHistory>1</EnableCallHistory>
        <LineDisplayFormat>$name@$protocol$instance</LineDisplayFormat>
        <EnableMWITone>0</EnableMWITone>
        <SIPNotifyXML>1</SIPNotifyXML>
        <BlockXMLWhenCall>1</BlockXMLWhenCall>
        <XMLUpdateInterval>30</XMLUpdateInterval>
        <VqmDisplayOrder></VqmDisplayOrder>
        <EnablePushXMLAuth>0</EnablePushXMLAuth>
        <PickupVisualAlert>0</PickupVisualAlert>
        <PickupAudioAlert>0</PickupAudioAlert>
        <PickupRingType></PickupRingType>
        <PbookDisplayAttr></PbookDisplayAttr>
        <DisplayBusinessCardTimeout>0</DisplayBusinessCardTimeout>
        <DisplayCallDuration>1</DisplayCallDuration>
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
            <DSTFixedType>2</DSTFixedType>
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
            <DateDisplayStyle>2</DateDisplayStyle>
            <DateSeparator>0</DateSeparator>
        </timeDisplay>
        {% if XX_xivo_phonebook_url -%}
        <softkey>
            <DesktopSoftkey>history;dss1;;menu;</DesktopSoftkey>
        </softkey>
        <xmlContact index="1">
            <Name>{{ XX_directory|d('Directory') }}</Name>
            <Addr>{{ XX_xivo_phonebook_url }}</Addr>
            <UserName></UserName>
            <PassWd></PassWd>
            <Sipline>-1</Sipline>
            <BindLine>-1</BindLine>
            <PhonebookType>0</PhonebookType>
        </xmlContact>
        {% endif %}
    </phone>
    <cti>
        {% if XX_wazo_phoned_user_service_dnd_enabled_url -%}
        <DNDOnUrl>{{ XX_wazo_phoned_user_service_dnd_enabled_url }}</DNDOnUrl>
        {% endif -%}
        {% if XX_wazo_phoned_user_service_dnd_disabled_url -%}
        <DNDOffUrl>{{ XX_wazo_phoned_user_service_dnd_disabled_url }}</DNDOffUrl>
        {% endif -%}
    </cti>
    <dsskey>
        <dssSide index="1">
            {%- if sip_lines %}
            {% for line_no in sip_lines -%}
            <Fkey index="{{ line_no }}">
                <Type>2</Type>
                <Value>SIP{{ line_no }}</Value>
                <Title></Title>
            </Fkey>
            {%- endfor %}
            {%- else %}
            <Fkey index="1">
                <Type>2</Type>
                <Value>SIP1</Value>
                <Title></Title>
            </Fkey>
            {%- endif %}
        </dssSide>
        {% if XX_paginated_fkeys -%}
            <FuncKeyPageNum>{{ XX_max_page }}</FuncKeyPageNum>
        {% for page, index, fkey in XX_paginated_fkeys -%}
        {% if loop.index0 == 0 or page != loop.previtem[0] -%}
        {% if loop.index0 != 0 -%}
        </dssSide>
        {%- endif %}
        <dssSide index="{{ page }}">
        {%- endif %}
            <Fkey index="{{ index }}">
            {%- if sip_lines %}
            {% for line_no in sip_lines -%}
                <Type>{{ fkey['type'] }}</Type>
                <Value>{{ fkey['value'] }}@SIP{{ line_no }}</Value>
                <Title>{{ fkey['title'] }}</Title>
            {%- endfor %}
            {%- endif %}
            </Fkey>
        {%- endfor %}
        </dssSide>
        {% endif -%}
        {% if XX_xivo_phonebook_url -%}
        <dssSoft index="1">
            <Type>21</Type>
            <Value>{{ XX_xivo_phonebook_url }}</Value>
            <Title>{{ XX_directory|d('Directory') }}</Title>
        </dssSoft>
        {%- endif %}
    </dsskey>
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
    <vpn>
        <VPNmode>-1</VPNmode>
        <EnableVPN>0</EnableVPN>
        <EnableNat>0</EnableNat>
        <Openvpnmode>0</Openvpnmode>
        <VPNConnectTimeout>60</VPNConnectTimeout>
        <OpenvpnEnableUserAuth>0</OpenvpnEnableUserAuth>
        <OpenvpnUserName></OpenvpnUserName>
        <OpenvpnPassword></OpenvpnPassword>
        <L2TPServerAddress>0.0.0.0</L2TPServerAddress>
        <L2TPUserName></L2TPUserName>
        <L2TPPassword></L2TPPassword>
        <L2TPNegotiateDNS>1</L2TPNegotiateDNS>
        <PPTPServerAddress>0.0.0.0</PPTPServerAddress>
        <PPTPUserName></PPTPUserName>
        <PPTPPassword></PPTPPassword>
        <SSTPServerAddress>0.0.0.0</SSTPServerAddress>
        <SSTPUserName></SSTPUserName>
        <SSTPPassword></SSTPPassword>
    </vpn>
    <ap>
        <DownloadCommonConf>0</DownloadCommonConf>
        <DownloadDeviceConf>1</DownloadDeviceConf>
        <SaveProvisionInfo>1</SaveProvisionInfo>
        <FlashServerIP>{{ XX_server_url }}</FlashServerIP>
        <FlashFileName>Fanvil/$mac.cfg</FlashFileName>
        <FlashProtocol>4</FlashProtocol>
        <FlashMode>1</FlashMode>
        <FlashInterval>1</FlashInterval>
        <pnp>
            <PNPEnable>0</PNPEnable>
        </pnp>
        <opt>
            <DHCPOption>66</DHCPOption>
        </opt>
    </ap>
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
</sysConf>

<?xml version="1.0" encoding="UTF-8"?>
<sysConf>
    <Version>2.0000000000</Version>
    {% if XX_fw_filename -%}
    <AUTOUPDATE_CONFIG_MODULE>
    <Download_Mode>1</Download_Mode>
    <Auto_Image_URL>http://{{ ip }}:{{ http_port }}/Fanvil/firmware/{{ XX_fw_filename }}</Auto_Image_URL>
    </AUTOUPDATE_CONFIG_MODULE>
    {% endif -%}
    <ap>
        <DownloadCommonConf>0</DownloadCommonConf>
        <DownloadDeviceConf>1</DownloadDeviceConf>
        <SaveProvisionInfo>1</SaveProvisionInfo>
        <FlashServerIP>{{ ip }}</FlashServerIP>
        <FlashFileName>Fanvil/$mac.cfg</FlashFileName>
        <FlashProtocol>4</FlashProtocol>
        <FlashMode>2</FlashMode>
        <FlashInterval>1</FlashInterval>
        <pnp>
            <PNPEnable>0</PNPEnable>
        </pnp>
        <opt>
            <DHCPOption>66</DHCPOption>
        </opt>
    </ap>
    <phone>
        <MenuPassword>{{ admin_password|d('123') }}</MenuPassword>
        <display>
            <DefaultLanguage>{{ XX_locale }}</DefaultLanguage>
            {% for line_no, line in sip_lines.iteritems() %}
            <LCDTitle>{{ line['display_name']|e }} {{ line['number'] }}</LCDTitle>
            {% endfor %}
        </display>
        <date>
            {% if ntp_enabled -%}
            <SNTPServer>{{ ntp_ip }}</SNTPServer>
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
            {% endif -%}
        </date>
        <timeDisplay>
            <TimeDisplayStyle>0</TimeDisplayStyle>
            <DateDisplayStyle>2</DateDisplayStyle>
        </timeDisplay>
        {% if XX_xivo_phonebook_url -%}
        <softkey>
            <DesktopSoftkey>history;dss1;;menu;</DesktopSoftkey>
        </softkey>
        {% endif %}
    </phone>
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
    <fwCheck>
        <EnableAutoUpgrade>0</EnableAutoUpgrade>
        <UpgradeServer1></UpgradeServer1>
        <UpgradeServer2></UpgradeServer2>
        <AutoUpgradeInterval>24</AutoUpgradeInterval>
    </fwCheck>
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
        {% for line_no, line in sip_lines.iteritems() -%}
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
        <dssSide index="1">
            <Fkey index="1">
                <Type>2</Type>
                <Value>SIP1</Value>
                <Title></Title>
                <ICON>Green</ICON>
            </Fkey>
        </dssSide>
        <internal index="1">
        {% for fkey in XX_fkeys -%}
            <Fkey index="{{ fkey['id'] }}">
                <Type>{{ fkey['type'] }}</Type>
                <Value>{{ fkey['value'] }}</Value>
                <Title>{{ fkey['title'] }}</Title>
                <ICON>Green</ICON>
            </Fkey>
        {% endfor -%}
        </internal>
        {% if XX_xivo_phonebook_url -%}
        <dssSoft index="1">
            <Type>21</Type>
            <Value>{{ XX_xivo_phonebook_url }}</Value>
            <Title>{{ XX_directory|d('Directory') }}</Title>
            <ICON>Green</ICON>
        </dssSoft>
        {% endif -%}
    </dsskey>
</sysConf>

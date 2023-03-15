<?xml version="1.0" encoding="UTF-8" ?>
<settings>
	
    <!-- Configuration du DM et Réseau  -->
    <setting id="LocalEnetcfgDmUrl" value="{{ XX_server_url }}" override="true"/> 
    <setting id="EdsEnetcfgDmUrl" value="{{ XX_server_url }}" override="true"/>
{% if vlan_enabled -%}
    <setting id="LocalEnetcfgVlanEnabl" value="true" override="true"/> 
    <setting id="LocalEnetcfgVlan" value="{{ vlan_id }}" override="true"/>
{% else -%}
    <setting id="LocalEnetcfgVlanEnabl" value="false" override="true"/>
    <setting id="LocalEnetcfgVlan" value="" override="true"/>
{% endif -%} 

    <!-- SIP mode -->
    <setting id="SipAppRunMode" value="0" override="true"/>
    <setting id="LocalAdmcfgRunMode" value="SIP" override="true"/>
	
    <!-- Phone Parameter	-->
    <setting id="DialingRuleCountryCode" value="*FR" override="true"/>
    <setting id="DialingRuleAreaCode" value="*{{ timezone }}" override="true"/>
    <setting id="DialingRuleExternalPrefix" value="0" override="true"/>
    <setting id="AudioToneCountry" value="{{ XX_lang }}" override="true"/>
    <setting id="SIPSrtpAuthentication" value="0" override="true"/>
    <setting id="TelephonyVmNumber" value="{{ exten_voicemail }}" />

    <!-- SIP Servers/Groups/Accounts -->
{% for line_no, line in sip_lines.items() -%}
    <setting id="SIPServer{{ line_no }}Address" value="{{ line['proxy_ip'] }}" override="true"/>
    <setting id="SIPGroup{{ line_no }}DomainName" value="{{ line['proxy_ip'] }}" override="true"/>
    <setting id="SIPGroup{{ line_no }}AuthenticationName" value="{{ line['auth_username']|d(line['username']) }}" override="true"/>
    <setting id="SIPGroup{{ line_no }}AuthenticationRealm" value="{{ line['auth_username']|d(line['username']) }}" override="true"/>
    <setting id="SIPGroup{{ line_no }}AuthenticationPassword" value="{{ line['password'] }}" override="true"/>
    <setting id="SIPGroup{{ line_no }}LabelName" value="{{ line['display_name'] }}" override="true"/>
    <setting id="SIPGroup{{ line_no }}DisplayName" value="{{ line['display_name'] }}" override="true"/>
    <setting id="SIPGroup{{ line_no }}ServerType" value="7" override="true"/>
    <setting id="SIPGroup{{ line_no }}DeviceUri" value="{{ line['auth_username']|d(line['username']) }}" override="true"/>
    {% if line['outbound_proxy_ip'] -%}
    <setting id="SIPGroup{{ line_no }}OutBoundProxyAddress" value="{{ line['outbound_proxy_ip'] }}" override="true"/>
    {% else -%}
    <setting id="SIPGroup{{ line_no }}OutBoundProxyAddress" value="" override="true"/>
    {% endif -%}
    {% if line['outbound_proxy_port'] -%}
    <setting id="SIPGroup{{ line_no }}OutBoundProxyPort" value="{{ line['outbound_proxy_port'] }}" />
    {% else -%}
    <setting id="SIPGroup{{ line_no }}OutBoundProxyPort" value="5060" />
    {% endif -%}
     <!-- Voicemail -->
     <setting id="SIPMessageWaitingIndicationUri" value="{{ line['voicemail'] }}" />
{% endfor -%}
    <!-- Programm Key -->
{% for fkey in XX_fkeys -%}
    <setting id="SIPUseDeviceKey{{ fkey['position'] }}" value="{{ fkey['value'] }}" />
{% endfor -%}
     <!-- NTP IP Address (CallServer) -->
{% if ntp_enabled -%}
     <setting id="LocalEnetcfgSntp" value="{{ ntp_ip }}" override="true"/>
     <setting id="DmAdmcfgTimeZone" value="{{ XX_timezone }}" override="true"/>
{% else -%}
     <setting id="LocalEnetcfgSntp" value="" override="true"/>
{% endif -%}
     <!-- Voice Codec -->
     <setting id="SIPPreferredVocoder" value="0;8;18;9;98;125" />
     <!-- Voice Settings -->
     <setting id="SIPRegisterExpire" value="180" />
     <setting id="SIPRegisterRetry" value="60" />
     <!-- Auto Answer -->
{% if XX_options['switchboard'] -%}
     <setting id="SIPAutoAnsweredAllowed" value="true" />
{% else -%}
     <setting id="SIPAutoAnsweredAllowed" value="false" />
{% endif -%}
     <!-- Admin Password  -->
     <setting id="WebUserPasswd" value="123789" override="true"/>
     <setting id="DmAdminPasswd" value="123456" override="true"/>
{% if user_password -%}
     <setting id="WebUserPasswd" value="{{ user_password|e }}" />
{% else -%}
     <setting id="WebUserPasswd" value="123789" />
{% endif -%}
{% if admin_password -%}
     <setting id="DmAdminPasswd" value="{{ admin_password|e }}" />
{% else -%}
     <setting id="DmAdminPasswd" value="123456" />
{% endif -%}

     <!-- Language -->
     <setting id="language_local" value="{{ XX_lang }}" override="true"/>
     <setting id="language" value="{{ XX_lang }}" override="true"/>
     <setting id="language_choice" value="true" override="true"/>
</settings>

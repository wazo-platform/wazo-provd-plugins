<?xml version="1.0" encoding="UTF-8"?>
<provisioning version="1.1" productID="e2">
    <firmware>
    {%- if http_port %}
        <file version="2.62.1" url="{{ XX_server_url }}/Gigaset-Nx70-V2.62.1-build.d1d6a22.bin"/>
    {%- endif %}
    </firmware>

    <nvm>
        <oper name="DeleteNotProvisionedHS"/>
    {%- if admin_password %}
        <param name="WebUIAccounts.1.Password" value="{{ admin_password }}"/>
    {%- endif %}
        <param name="Telephony.0.ToneScheme" value="{{ XX_country }}"/>

    {%- if http_port %}
        <param name="Provisioning.global.ProvisioningServer" value="{{ XX_server_url }}"/>
    {%- endif %}

        <!-- Nx70 Telephony - Call settings -->
        <param name="Telephony.0.CT_ViaRKey" value="1"/>
        <param name="Telephony.0.CT_ByOnHook" value="1"/>

        <param name="DmGlobal.0.SuotaEnable" value="1"/>
        <param name="DmGlobal.0.HSIdleDisplay" value="1"/>
        <param name="DmGlobal.0.SystemRegDomain" value="EUR"/>

        <param name="dm.local.FwUpdateCallBlockAttempts" value="288" />


        <!-- Date and time -->
    {%- if ntp_enabled %}
        <param name="DmGlobal.0.NtpServer" value="{{ ntp_ip }}"/>
    {%- endif %}

    {%- if timezone %}
        <param name="DmGlobal.0.TimeZone" value="{{ timezone }}"/>
    {%- endif %}

{%- if sip_lines %}
    {%- for line_no, line in sip_lines.items() %}
        {%- set handset_no = line_no.zfill(5) %}
        <!-- Handset {{ line_no }} -->
        <oper value="{{ handset_no }}" name="add_hs">
            <param name="hs.RegStatus" value="ToReg"/>
        </oper>

        <param name="hs.{{ handset_no }}.DECT_AC" value="{{ line['XX_hs_code'] }}"/>
        <param name="SipAccount.{{ handset_no }}.AuthName" value="{{ line['auth_username']|d(line['username']) }}"/>
        <param name="SipAccount.{{ handset_no }}.AuthPassword" value="{{ line['auth_password']|d(line['password']) }}"/>
        <param name="SipAccount.{{ handset_no }}.ProviderId" value="{{ line['provider_id'] }}"/>
        <param name="SipAccount.{{ handset_no }}.UserName" value="{{ line['auth_username']|d(line['username']) }}"/>
        <param name="SipAccount.{{ handset_no }}.DisplayName" value="{{ line['number'] }} {{ line['display_name'] }}"/>
        {%- if line['voicemail'] %}
        <param name="SipAccount.{{ handset_no }}.VoiceMailMailbox" value="{{ line['voicemail'] }}"/>
        <param name="SipAccount.{{ handset_no }}.VoiceMailActive" value="1"/>
        {%- endif %}
        <param name="hs.{{ handset_no }}.DirectAccessDir" value="0"/>
        <param name="hs.{{ handset_no }}.IntKeyDir" value="20"/>

    {%- endfor %}
{%- endif %}

{%- for provider in XX_voip_providers %}
        <!-- VoIP Provider {{ provider['id'] }} settings -->

        <param name="SipProvider.{{ provider['id'] }}.Name" value="Wazo{{ provider['id'] }}"/>

        <!-- General data of your service provider -->

    {%- if provider['sip_proxy_ip'] %}
        <param name="SipProvider.{{ provider['id'] }}.Domain" value="{{ provider['sip_proxy_ip'] }}"/>
        <param name="SipProvider.{{ provider['id'] }}.ProxyServerAddress" value="{{ provider['sip_proxy_ip'] }}"/>
        <param name="SipProvider.{{ provider['id'] }}.ProxyServerPort" value="{{ provider['sip_proxy_port']|d(5060) }}"/>
    {%- endif %}
    {%- if sip_registrar_ip %}
        <param name="SipProvider.{{ provider['id'] }}.RegServerAddress" value="{{ sip_registrar_ip }}"/>
        <param name="SipProvider.{{ provider['id'] }}.RegServerPort" value="{{ sip_registrar_port|d(5060) }}"/>
    {%- endif %}
        <param name="SipProvider.{{ provider['id'] }}.RegServerRefreshTimer" value="180"/>
        <param name="SipProvider.{{ provider['id'] }}.TransportProtocol" value="{{ provider['sip_transport'] }}"/>
        <param name="SipProvider.{{ provider['id'] }}.UseSIPS" value="0"/>
    {%- if provider['sip_transport'] == '3' %}
        <param name="SipProvider.{{ provider['id'] }}.SRTP_Enabled" value="1"/>
    {%- else %}
        <param name="SipProvider.{{ provider['id'] }}.SRTP_Enabled" value="0"/>
    {%- endif %}
        -->
        <param name="SipProvider.{{ provider['id'] }}.AcceptNonSRTPCalls" value="0"/>
        <param name="SipProvider.{{ provider['id'] }}.DTMFTransmission" value="{{ provider['dtmf_mode'] }}"/>
        <param name="SipProvider.{{ provider['id'] }}.WithDeregOnHsNotReachable" value="1"/>

        <!-- Redundancy -->

        <param name="SipProvider.{{ provider['id'] }}.DnsQuery" value="0"/>

        <!-- Failover Server -->
    {%- if sip_backup_proxy_ip %}
        <param name="SipProvider.{{ provider['id'] }}.FailoverServerEnabled" value="1"/>
        <param name="SipProvider.{{ provider['id'] }}.FailoverServerAddress" value="{{ sip_backup_proxy_ip }}"/>
        <param name="SipProvider.{{ provider['id'] }}.FailoverServerPort" value="{{ sip_backup_proxy_port|d(5060) }}"/>
    {%- else %}
        <param name="SipProvider.{{ provider['id'] }}.FailoverServerEnabled" value="0"/>
    {%- endif %}
{%- endfor %}

        <!-- Directory -->
        <param name="Netdir.1.Activated" value="1"/>
        <param name="XMLDir.1.ProviderName" value="Wazo"/>
        <param name="XMLDir.1.ServerURL" value="{{ XX_xivo_phonebook_url }}"/>
        <param name="XMLDir.1.WhitePagesDirName" value="Directory"/>
        <param name="XMLDir.1.StartWithListWP" value="1"/>
        <!-- Network data of your service provider -->

    {%- if sip_outbound_proxy_ip %}
        <param name="SipProvider.0.OutboundProxyMode" value="0"/>
        <param name="SipProvider.0.OutboundProxyAddress" value="{{ sip_outbound_proxy_ip }}"/>
        <param name="SipProvider.0.OutboundProxyPort" value="{{ sip_outbound_proxy_port|d(5060) }}"/>
    {%- else %}
        <param name="SipProvider.0.OutboundProxyMode" value="2"/>
    {%- endif %}
    {%- if sip_subscribe_mwi %}
        <param name="SipProvider.0.MWISubscription" value="1"/>
    {%- else %}
        <param name="SipProvider.0.MWISubscription" value="0"/>
    {%- endif %}

        <oper name="update_dm" value="local">
            <param name="RegStart" value="{{ XX_epoch }}"/>
            <param name="RegDuration" value="900"/>
            <param name="DMPpasswd" value="Gigaset"/>
        </oper>
    </nvm>

</provisioning>

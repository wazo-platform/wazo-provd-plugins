<?xml version="1.0" encoding="UTF-8"?>
<provisioning version="1.1" productID="e2">
    <firmware>
        <file version="2.14.0" url="http://192.168.178.200/firmware/n870/einstein-albert-V2.14.0+build.74f2b0e.update.bin" />
    </firmware>

    <nvm>

        <param name="Telephony.0.ToneScheme" value="Germany"/>

    {%- if http_port %}
        <param name="Provisioning.global.ProvisioningServer" value="http://{{ ip }}:{{ http_port }}"/>
    {%- endif %}

        <!-- N870 Telephony - Call settings -->
        <param name="Telephony.0.CT_ViaRKey" value="1"/>
        <param name="Telephony.0.CT_ByOnHook" value="1"/>


        <param name="DmGlobal.0.HSIdleDisplay" value="1"/>


        <!-- Date and time -->
    {%- if ntp_enabled %}
        <param name="DmGlobal.0.NtpServer" value="{{ ntp_ip }},0.europe.pool.ntp.org,1.europe.pool.ntp.org,2.europe.pool.ntp.org,3.europe.pool.ntp.org"/>
        <param name="DmGlobal.0.TimeZone" value="{{ XX_timezone }}"/>
    {%- endif %}


{%- if sip_lines %}
    {%- for line_no, line in sip_lines.iteritems() %}
        {%- set handset_no = line_no.zfill(5) %}
        <!-- Handset {line_no} -->
        <oper value="{{ handset_no }}" name="add_hs">

            <param name="hs.RegStatus" value="ToReg"/>

        </oper>

        <param name="SipAccount.{{ handset_no }}.AuthName" value="{{ line['auth_username']|d(line['username']) }}" />
        <param name="SipAccount.{{ handset_no }}.AuthPassword" value="{{ line['auth_password']|d(line['password']) }}" />
        <param name="SipAccount.{{ handset_no }}.UserName" value="{{ line['auth_username']|d(line['username']) }}" />
        <param name="SipAccount.{{ handset_no }}.DisplayName" value="{{ line['number'] }}" />
        {%- if line['voicemail'] %}
        <param name="SipAccount.{{ handset_no }}.VoiceMailMailbox" value="{{ line['voicemail'] }}" />
        <param name="SipAccount.{{ handset_no }}.VoiceMailActive" value="1" />
        {%- endif %}
        <param name="SipAccount.{{ handset_no }}.ProviderId" value="0" />
        <param name="hs.{{ handset_no }}.DirectAccessDir" value="0" />
        <param name="hs.{{ handset_no }}.DECT_AC" value="{{ line['number'][-4:] }}" />

    {%- endfor %}
{%- endif %}
        <!-- VoIP Provider 1 settings -->

        <param name="SipProvider.0.Name" value="Wazo"/>

        <!-- General data of your service provider -->

    {%- if sip_proxy_ip %}
        <param name="SipProvider.0.Domain" value="{{ sip_proxy_ip }}"/>
        <param name="SipProvider.0.ProxyServerAddress" value="{{ sip_proxy_ip }}"/>
        <param name="SipProvider.0.ProxyServerPort" value="{{ sip_proxy_port|d(5060) }}"/>
    {%- endif %}
    {%- if sip_registrar_ip %}
        <param name="SipProvider.0.RegServerAddress" value="{{ sip_registrar_ip }}"/>
        <param name="SipProvider.0.RegServerPort" value="{{ sip_registrar_port|d(5060) }}"/>
    {%- endif %}
        <param name="SipProvider.0.RegServerRefreshTimer" value="180"/>
        <param name="SipProvider.0.TransportProtocol" value="1"/>
        <param name="SipProvider.0.UseSIPS" value="0"/>
        <param name="SipProvider.0.SRTP_Enabled" value="0"/>
        <param name="SipProvider.0.AcceptNonSRTPCalls" value="0"/>

        <!-- Redundancy -->

        <param name="SipProvider.0.DnsQuery" value="0"/>

        <!-- Failover Server -->
    {%- if sip_backup_proxy_ip %}
        <param name="SipProvider.0.FailoverServerEnabled" value="1"/>
        <param name="SipProvider.0.FailoverServerAddress" value="{{ sip_backup_proxy_ip }}"/>
        <param name="SipProvider.0.FailoverServerPort" value="{{ sip_backup_proxy_port|d(5060) }}"/>
    {%- else %}
        <param name="SipProvider.0.FailoverServerEnabled" value="0"/>
    {%- endif %}

        <!-- Network data of your service provider -->

    {%- if sip_outbound_proxy_ip %}
        <param name="SipProvider.0.OutboundProxyMode" value="0"/>
        <param name="SipProvider.0.OutboundProxyAddress" value="{{ sip_outbound_proxy_ip }}"/>
        <param name="SipProvider.0.OutboundProxyPort" value="{{ sip_outbound_proxy_port|d(5060) }}"/>
        <param name="SipProvider.0.MWISubscription" value="0"/>
    {%- else %}
        <param name="SipProvider.0.OutboundProxyMode" value="2"/>
    {%- endif %}

    </nvm>

</provisioning>

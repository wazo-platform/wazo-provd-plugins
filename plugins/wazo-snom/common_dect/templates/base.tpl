<?xml version="1.0" encoding="utf-8" ?>
<settings>
    <phone-settings>
    {%- if vlan_enabled %}
        <vlan_id>{{ vlan_id }}</vlan_id>
        <vlan_qos>{{ vlan_priority|d('0') }}</vlan_qos>
    {%- else %}
        <vlan_id></vlan_id>
        <vlan_qos></vlan_qos>
    {%- endif %}

        <codec_tos>184</codec_tos>
        <signaling_tos>184</signaling_tos>

    {%- if admin_username %}
        <http_user>{{ admin_username|e }}</http_user>
    {%- else %}
        <http_user>guest</http_user>
    {%- endif %}

    {%- if admin_password %}
        <admin_mode_password>{{ admin_password|e }}</admin_mode_password>
        <http_pass>{{ admin_password|e }}</http_pass>
    {%- else %}
        <admin_mode_password>12345</admin_mode_password>
        <http_pass>guest</http_pass>
    {%- endif %}

    {%- if ntp_enabled %}
        <ntp_server>{{ ntp_ip }}</ntp_server>
    {%- else %}
        <ntp_server></ntp_server>
    {%- endif %}

    {%- for server in XX_servers.values() %}
        <srv_sip_server_alias idx="{{ server['id'] }}">Wazo {{ server['id'] }}</srv_sip_server_alias>
        <user_host idx="{{ server['id'] }}">{{ server['proxy_ip'] }}</user_host>
        <srv_srtp_auth idx="{{ server['id'] }}">off</srv_srtp_auth>
        <user_dtmf_info idx="{{ server['id'] }}">{{ server['dtmf_mode'] }}</user_dtmf_info>
    {%- endfor %}

    {%- for line_no, line in sip_lines.iteritems() %}
        <user_active idx="{{ line_no }}">on</user_active>
        <user_name idx="{{ line_no }}">{{ line['username']|e }}</user_name>
        <user_pname idx="{{ line_no }}">{{ line['auth_username']|e }}</user_pname>
        <user_pass idx="{{ line_no }}">{{ line['password']|e }}</user_pass>
        <user_realname idx="{{ line_no }}">{{ line['display_name']|e }}</user_realname>
        <user_mailbox idx="{{ line_no }}">{{ line['voicemail'] }}</user_mailbox>
        <subscr_sip_hs_idx idx="{{ line_no }}">{{ line_no }}</subscr_sip_hs_idx>
        <subscr_dect_ac_code idx="{{ line_no }}">{{ "{0:0>4}".format(line_no) }}</subscr_dect_ac_code>
        <subscr_sip_ua_data_server_id idx="{{ line_no }}">{{ line['XX_server_id'] }}</subscr_sip_ua_data_server_id>
    {%- endfor %}

    {% if XX_xivo_phonebook_url -%}
        <phonebook_server_location perm="R">3</phonebook_server_location>
        <phonebook_location perm="R">{{ XX_xivo_phonebook_url|e }}</phonebook_location>
    {% endif -%}

    {%- if XX_lang %}
        <language>{{ XX_lang[0] }}</language>
        <web_language>{{ XX_lang[0] }}</web_language>
        <tone_scheme>{{ XX_lang[1] }}</tone_scheme>
    {%- endif %}

    {% block settings_suffix %}{% endblock %}
    </phone-settings>
</settings>

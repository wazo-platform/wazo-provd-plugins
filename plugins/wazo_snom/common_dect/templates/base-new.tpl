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
        <codec_priority_list perm="R">pcma,pcmu,g722,g729,telephone-event</codec_priority_list>
        <signaling_tos>184</signaling_tos>

    {%- if admin_username %}
        <http_user>{{ admin_username|e }}</http_user>
        <http_engineer_user>Engineer</http_engineer_user>
    {%- else %}
        <http_user>admin</http_user>
        <http_engineer_user>Engineer</http_engineer_user>
    {%- endif %}

    {%- if admin_password %}
        <http_pass>{{ admin_password|e }}</http_pass>
        <http_engineer_pass>{{ admin_password|e }}</http_engineer_pass>
    {%- else %}
        <http_pass>wazo!2025</http_pass>
        <http_engineer_pass>wazo!2025</http_engineer_pass>
    {%- endif %}

    {%- if user_username %}
        <http_basic_user>{{ user_username|e }}</http_basic_user>
    {%- else %}
        <http_basic_user>User</http_basic_user>
    {%- endif %}

    {%- if user_password %}
        <http_basic_pass>{{ user_password|e }}</http_basic_pass>
    {%- else %}
        <http_basic_pass>wazo!2025</http_basic_pass>
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

    {%- for line_no, line in sip_lines.items() %}
        <user_active idx="{{ line_no }}">on</user_active>
        <user_name idx="{{ line_no }}">{{ line['username']|e }}</user_name>
        <user_pname idx="{{ line_no }}">{{ line['auth_username']|e }}</user_pname>
        <user_pass idx="{{ line_no }}">{{ line['password']|e }}</user_pass>
        <user_realname idx="{{ line_no }}">{{ line['display_name']|e }}</user_realname>
        <user_mailbox idx="{{ line_no }}">Messagerie</user_mailbox>
        <user_mailnumber idx="{{ line_no }}">{{ line['voicemail'] }}</user_mailnumber>
        <subscr_sip_line_name idx="{{ line_no }}">{{ line['number']|e }}</subscr_sip_line_name>
        <subscr_sip_hs_idx idx="{{ line_no }}">{{ line_no }}</subscr_sip_hs_idx>
        <subscr_dect_ac_code idx="{{ line_no }}">{{ "{0:0>4}".format(line_no) }}</subscr_dect_ac_code>
        <subscr_sip_ua_data_server_id idx="{{ line_no }}">{{ line['XX_server_id'] }}</subscr_sip_ua_data_server_id>
        <codec_priority_list idx="{{ line_no }}" perm="R">pcma,pcmu,g722,g729,telephone-event</codec_priority_list>
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

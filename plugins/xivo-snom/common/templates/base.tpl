<?xml version="1.0" encoding="UTF-8" ?>
<settings>
  <phone-settings>
    {% if vlan_enabled -%}
    <vlan_id perm="R">{{ vlan_id }}</vlan_id>
    <vlan_qos perm="R">{{ vlan_priority|d('0') }}</vlan_qos>
    {% else -%}
    <vlan_id perm="R"></vlan_id>
    <vlan_qos perm="R"></vlan_qos>
    {% endif -%}
    
    <codec_tos perm="R">184</codec_tos> 
    <signaling_tos perm="R">184</signaling_tos>

    {% if admin_username -%}
    <http_user perm="R">{{ admin_username|e }}</http_user>
    {% else -%}
    <http_user perm="R">guest</http_user>
    {% endif -%}

    {% if admin_password -%}
    <admin_mode_password perm="R">{{ admin_password|e }}</admin_mode_password>
    <http_pass perm="R">{{ admin_password|e }}</http_pass>
    {% else -%}
    <admin_mode_password perm="R">12345</admin_mode_password>
    <http_pass perm="R">guest</http_pass>
    {% endif -%}

    {% if ntp_enabled -%}
    <ntp_server perm="R">{{ ntp_ip }}</ntp_server>
    {% else -%}
    <ntp_server perm="R"></ntp_server>
    {% endif -%}

    {% for line_no, line in sip_lines.iteritems() %}
    <user_active idx="{{ line_no }}" perm="R">on</user_active>
    <user_idle_text idx="{{ line_no }}" perm="R">{{ line['display_name']|e }} {{ line['number'] }}</user_idle_text>
    <user_host idx="{{ line_no }}" perm="R">{{ line['proxy_ip'] }}</user_host>
    <user_name idx="{{ line_no }}" perm="R">{{ line['username']|e }}</user_name>
    <user_pname idx="{{ line_no }}" perm="R">{{ line['auth_username']|e }}</user_pname>
    <user_pass idx="{{ line_no }}" perm="R">{{ line['password']|e }}</user_pass>
    <user_realname idx="{{ line_no }}" perm="R">{{ line['display_name']|e }}</user_realname>
    <user_mailbox idx="{{ line_no }}" perm="R">{{ line['voicemail'] }}</user_mailbox>
    <user_dtmf_info idx="{{ line_no }}" perm="R">{{ line['XX_user_dtmf_info'] }}</user_dtmf_info>

    {% if line['backup_proxy_ip'] -%}
    <user_failover_identity idx="{{ line_no }}" perm="R">{{ line_no|int + 1 }}</user_failover_identity>

    <user_active idx="{{ line_no|int + 1 }}" perm="R">on</user_active>
    <user_idle_text idx="{{ line_no|int + 1 }}" perm="R">{{ line['display_name']|e }} {{ line['number'] }}</user_idle_text>
    <user_host idx="{{ line_no|int + 1 }}" perm="R">{{ line['backup_proxy_ip'] }}</user_host>
    <user_name idx="{{ line_no|int + 1 }}" perm="R">{{ line['username']|e }}</user_name>
    <user_pname idx="{{ line_no|int + 1 }}" perm="R">{{ line['auth_username']|e }}</user_pname>
    <user_pass idx="{{ line_no|int + 1 }}" perm="R">{{ line['password']|e }}</user_pass>
    <user_realname idx="{{ line_no|int + 1 }}" perm="R">{{ line['display_name']|e }}</user_realname>
    <user_mailbox idx="{{ line_no|int + 1 }}" perm="R">{{ line['voicemail'] }}</user_mailbox>
    <user_dtmf_info idx="{{ line_no|int + 1 }}" perm="R">{{ line['XX_user_dtmf_info'] }}</user_dtmf_info>
    <hide_identity idx="{{ line_no|int + 1 }}" perm="R">true</hide_identity>
    {% endif -%}

    {% endfor -%}

    {% if XX_xivo_phonebook_url -%}
    <dkey_directory perm="R">url {{ XX_xivo_phonebook_url|e }}</dkey_directory>
    {% block gui_fkey1 %}
    <gui_fkey1 perm="R">
        <initialization>
            <variable name="label" value="{{ XX_dict['remote_directory'] }}"/>
        </initialization>
        <action>
            <url target="{{ XX_xivo_phonebook_url|e }}" when="on press"/>
        </action>
    </gui_fkey1>
    {% endblock %}
    {% endif -%}

    {% if XX_lang -%}
    <language perm="R">{{ XX_lang[0] }}</language>
    <web_language perm="R">{{ XX_lang[0] }}</web_language>
    <tone_scheme perm="R">{{ XX_lang[1] }}</tone_scheme>
    {% endif -%}

    {{ XX_timezone }}

    <!-- hide the "identity not registered" msg when Wazo HA is enabled -->
    <status_msgs_that_are_blocked perm="R">PhoneHasVoiceMessages PhoneHasTextMessages{{ XX_msgs_blocked }}</status_msgs_that_are_blocked>

    <call_waiting perm="R">{{ 'off' if XX_options['switchboard'] else 'on' }}</call_waiting>

    {% block settings_suffix %}{% endblock %}
  </phone-settings>
  <functionKeys>
    {% block fkeys_prefix %}{% endblock %}
    {{ XX_fkeys }}
  </functionKeys>
</settings>

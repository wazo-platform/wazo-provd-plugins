<?xml version="1.0" ?>
<config>
    <setting id="login_password" value="{{ admin_password|d(789) }}" />

    {% if timezone %}
    <setting id="time_zone" value="{{ timezone }}" />
    {% endif %}

    {% if ntp_enabled %}
    <setting id="time_source" value="ntp" />
    <setting id="ntp_server" value="{{ ntp_ip }}" />
    <setting id="ntp_resync" value="86400" />
    {% endif %}

    <setting id="accept_local_calls" value="any" />
    <setting id="backlight_timeout" value="30" />
    <setting id="ehs" value="Plantronics" />
    <setting id="enable_blf_on_unused_line_keys" value="1" />
    <setting id="blf_contact_group" value="Default" />

    {% if vlan_enabled %}
    <setting id="network_vlan_qos" value="{{ vlan_priority|d(0) }}" />
    <setting id="network_vlan_id" value="{{ vlan_id }}" />
    {% else %}
    <setting id="network_vlan_qos" value="0" />
    <setting id="network_vlan_id" value="0" />
    {% endif %}

    <contacts url="http://{{ ip }}:{{ http_port }}/Digium/{{ XX_mac }}-contacts.xml" id="internal" />

    <accounts>
        {% for line_no, line in sip_lines.iteritems() %}
        <account
        index="{{ line_no|int - 1 }}"
        status="1"
        register="1"
        account_id="{{ line['username'] }}"
        username="{{ line['username'] }}"
        authname="{{ line['auth_username'] }}"
        password="{{ line['password'] }}"
        line_label="{{ line['display_name'] }}"
        dial_plan="x.T6"
        visual_voicemail="0"
        {% if exten_voicemail %}
        voicemail="sip:{{ exten_voicemail }}@{{ line['proxy_ip'] }}"
        {% else %}
        voicemail=""
        {% endif %}
        conflict="replace">

            <host_primary
            server="{{ line['proxy_ip'] }}"
            port="{{ line['proxy_port']|d(5060) }}"
            transport="udp"
            reregister="3600"
            retry="25"
            num_retries="5" />

        </account>
        {% endfor %}
    </accounts>

    <firmwares>
        {% block firmwares %}{% endblock %}
    </firmwares>

    {% block suffix %}{% endblock %}
</config>

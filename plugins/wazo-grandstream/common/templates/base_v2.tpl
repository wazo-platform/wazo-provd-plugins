<?xml version="1.0" encoding="UTF-8" ?>
<gs_provision version="1">
 <config version="2">
    {% if admin_password -%}
    <item name="users.admin.password">{{ admin_password|e }}</item>
    {% endif -%}
    {% if ntp_enabled -%}
    <item name="dateTime.ntp.server.1">{{ ntp_ip }}</item>
    {% endif -%}
    {% if XX_timezone -%}
    <item name="dateTime.timezone">{{ XX_timezone }}</item>
    {% endif -%}
    {% if XX_locale -%}
    <item name="language.gui">{{ XX_locale }}</item>
    {% endif -%}
    {% if vlan_enabled -%}
    <item name="network.port.eth.1.vlan.tag">{{ vlan_id }}</item>
    {% endif -%}
    {% if vlan_priority is defined -%}
    <item name="network.port.eth.1.vlan.priority">{{ vlan_priority }}</item>
    {% endif -%}

    {% if dns_enabled -%}
    <item name="network.dns.preferred.ip.1">{{ XX_dns_1 }}</item>
    <item name="network.dns.preferred.ip.2">{{ XX_dns_2 }}</item>
    <item name="network.dns.preferred.ip.3">{{ XX_dns_3 }}</item>
    <item name="network.dns.preferred.ip.4">{{ XX_dns_4 }}</item>
    {% endif -%}
    {# Auto-upgrade firmware, check every day #}
    <item name="provisioning.auto.mode">YesUpgradeHourOfDay</item>
    <item name="provisioning.auto.randomTime.enable">Yes</item>
    {# Check firmware update between 23:00 and 01:00 #}
    <item name="provisioning.auto.hour">23</item>
    <item name="provisioning.auto.endHour">1</item>
    <item name="provisioning.firmware.confirm.enable">No</item>

{# SIP per-line settings -#}
{% for line_no, line in sip_lines.iteritems() %}
    <item name="account.{{ line_no }}.enable">Yes</item>
    <item name="account.{{ line_no }}.sip.registration">Yes</item>
    <item name="account.{{ line_no }}.sip.unregisterOnReboot">Yes</item>
    <item name="account.{{ line_no }}.call.dialplan">{ [*x]+ }</item>
    <item name="account.{{ line_no }}.intercom.allowAutoAnswer">Yes</item>
    {% if exten_pickup_call -%}
    <item name="account.{{ line_no }}.sip.blf.callPickup.prefix">{{ exten_pickup_call }}</item>
    {% endif -%}
    <item name="account.{{ line_no }}.name">{{ line['display_name'] }}</item>
    {% if XX_sip_transport -%}
    <item name="account.{{ line_no }}.sip.transport">{{ XX_sip_transport }}</item>
    {% endif -%}
    <item name="account.{{ line_no }}.sip.server.1.address">{{ line['registrar_ip'] }}</item>
    <item name="account.{{ line_no }}.sip.server.2.address">{{ line['backup_registrar_ip'] }}</item>
    <item name="account.{{ line_no }}.sip.userid">{{ line['auth_username'] }}</item>
    <item name="account.{{ line_no }}.sip.subscriber.userid">{{ line['auth_username'] }}</item>
    <item name="account.{{ line_no }}.sip.subscriber.password">{{ line['password'] }}</item>
    <item name="account.{{ line_no }}.sip.subscriber.name">{{ line['display_name'] }}</item>
    <item name="account.{{ line_no }}.sip.accountDisplay">User Name</item>
    <item name="account.{{ line_no }}.sip.voicemail.number">{{ exten_voicemail }}</item>
    <item name="account.{{ line_no }}.dtmf.sendInAudio">{{ XX_dtmf_in_audio }}</item>
    <item name="account.{{ line_no }}.dtmf.sendInRtp">{{ XX_dtmf_in_rtp }}</item>
    <item name="account.{{ line_no }}.dtmf.sendInSip">{{ XX_dtmf_in_sip }}</item>
    <item name="account.{{ line_no }}.featureCodes.callFeatures">No</item>
{% endfor -%}
{% if XX_v2_fkeys -%}
  {% for number, fkey in XX_v2_fkeys -%}
    {% if fkey['section'] == 'mpk' -%}
    <item name="pks.{{ fkey['section'] }}.{{ number }}.account">Account1</item>
    {% else -%}
    <item name="pks.{{ fkey['section'] }}.{{ number }}.account">0</item>
    {% endif -%}
    <item name="pks.{{ fkey['section'] }}.{{ number }}.keyMode">{{ fkey['type'] }}</item>
    <item name="pks.{{ fkey['section'] }}.{{ number }}.description">{{ fkey['label'] }}</item>
    <item name="pks.{{ fkey['section'] }}.{{ number }}.value">{{ fkey['value'] }}</item>
  {% endfor -%}
{% endif -%}
  </config>
</gs_provision>

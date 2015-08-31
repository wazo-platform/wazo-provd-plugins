<device>
 <devicePool>
  <dateTimeSetting>
   <dateTemplate>D-M-YA</dateTemplate>
   <timeZone>{{ XX_timezone }}</timeZone>
   <ntps>
    {% if ntp_enabled -%}
    <ntp>
     <name>{{ ntp_ip }}</name>
     <ntpMode>Unicast</ntpMode>
    </ntp>
   {% endif -%}
   </ntps>
  </dateTimeSetting>
  <callManagerGroup>
   <members>
    {% for call_manager in sccp_call_managers.itervalues() -%}
    <member priority="{{ call_manager['XX_priority'] }}">
     <callManager>
      <ports>
       <ethernetPhonePort>{{ call_manager['port']|d('2000') }}</ethernetPhonePort>
      </ports>
      <processNodeName>{{ call_manager['ip'] }}</processNodeName>
     </callManager>
    </member>
   {% endfor -%}
   </members>
  </callManagerGroup>
  <srstInfo>
   <srstOption>Disable</srstOption>
  </srstInfo>
 </devicePool>
 <versionStamp>{Dec 17 2010 16:03:58}</versionStamp>
 <loadInformation>{% block loadInformation %}{% endblock %}</loadInformation>
 <addOnModules>{{ XX_addons }}</addOnModules>

 {% if XX_locale -%}
 <userLocale>
  <name>i18n/{{ XX_locale[0] }}</name>
  <langCode>{{ XX_locale[1] }}</langCode>
 </userLocale>
 <networkLocale>i18n/{{ XX_locale[2] }}</networkLocale>
 {% endif -%}

 <idleTimeout>0</idleTimeout>
 <authenticationURL></authenticationURL>
 {% if X_xivo_phonebook_ip -%}
  {% if config_version|d(0) >= 1 -%}
   <directoryURL>http://{{ X_xivo_phonebook_ip }}:{{ X_xivo_phonebook_port|d(9498) }}/0.1/directories/menu?vendor=cisco{{ '&amp;xivo_user_uuid={}'.format(X_xivo_user_uuid) if X_xivo_user_uuid }}</directoryURL>
  {% else -%}
   {# backward compatibility URL with XiVO 15.14 or earlier -#}
   <directoryURL>http://{{ X_xivo_phonebook_ip }}/service/ipbx/web_services.php/phonebook/menu</directoryURL>
  {% endif -%}
 {% else -%}
 <directoryURL></directoryURL>
 {% endif -%}
 <idleURL></idleURL>
 <informationURL></informationURL>
 <messagesURL></messagesURL>
 <proxyServerURL></proxyServerURL>
 <servicesURL></servicesURL>
 <vendorConfig>
  <disableSpeaker>false</disableSpeaker>
  <disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
  <enableGroupListen>true</enableGroupListen>
 </vendorConfig>
</device>

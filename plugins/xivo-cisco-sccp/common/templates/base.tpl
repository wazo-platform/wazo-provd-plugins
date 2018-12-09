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
 <addOnModules>
 {% if XX_addons -%}
 {% for addon in XX_addons.itervalues() -%}
  <addOnModule idx="{{ addon['idx'] }}">
    <deviceType>{{ addon['type'] }}</deviceType>
    <deviceLine>{{ addon['line'] }}</deviceLine>
    <loadInformation>{{ addon['loadInformation'] }}</loadInformation>
  </addOnModule>
 {% endfor -%}
 {% endif -%}
 </addOnModules>

 {% if XX_locale -%}
 <userLocale>
  <name>i18n/{{ XX_locale[0] }}</name>
  <langCode>{{ XX_locale[1] }}</langCode>
 </userLocale>
 <networkLocale>i18n/{{ XX_locale[2] }}</networkLocale>
 {% endif -%}

 <idleTimeout>0</idleTimeout>
 <authenticationURL></authenticationURL>
 <directoryURL>{{ XX_xivo_phonebook_url|e }}</directoryURL>
 <idleURL></idleURL>
 <informationURL></informationURL>
 <messagesURL></messagesURL>
 <proxyServerURL></proxyServerURL>
 <servicesURL></servicesURL>
 <vendorConfig>
  <disableSpeaker>false</disableSpeaker>
  <disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
  <enableGroupListen>true</enableGroupListen>
  <g722CodecSupport>2</g722CodecSupport>
 </vendorConfig>
 <advertiseG722Codec>1</advertiseG722Codec>
</device>

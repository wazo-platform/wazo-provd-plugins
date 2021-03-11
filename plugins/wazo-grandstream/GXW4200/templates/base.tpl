<?xml version="1.0" encoding="UTF-8" ?>
<gs_provision version="1">
 <mac>{{ XX_mac }}</mac>
 <config version="1">
    <!-- Allow DHCP Option 66 to override server. 0 - No, 1 - Yes. Default is Yes. -->
    <!-- When set to Yes(1), it will override the configured provision path and method. -->
    <!-- Number: 0,1 -->
    <!-- Mandatory -->
    <!-- Reboot required -->
    <P145>1</P145>

    <!-- Use firmware pre/postfix to determine if f/w is required -->
    <!-- 0=Always Check for New Firmware -->
    <!-- 1=Check New Firmware only when F/W pre/suffix changes -->
    <!-- 2=Always Skip the Firmware Check -->
    <!-- For Firmware only. -->
    <!-- Number: 0,1,2 -->
    <!-- Mandatory -->
    <P238>0</P238>

    <!-- Automatic Upgrade. 0 - No, 1 - Check every () minutes, 2 - Check daily, 3 - Check weekly,. Default is No. -->
    <!-- Number: 0,1,2,3 -->
    <!-- Mandatory -->
    <P22296>1</P22296>

    <!-- <P194>3</P194> -->
    <!-- Automatic Upgrade. Check for new firmware/config file every () minutes, unit is in minute, minimum 60 minutes, default is 7 days. P194=3 -->
    <!-- Number: 60 to 5256000 -->
    <!-- Mandatory -->
    <P193>60<P193>

    <!-- Maintenance-Web/Telnet Access -->

    <!-- HTTP Web Port. Default HTTP is 80. -->
    <!-- Number: 1 to 65535 -->
    <!-- Mandatory -->
    <!-- Reboot required -->
    <P901>80</P901>

    <!-- HTTPS Web Port. Default HTTPS Port is 443 -->
    <!-- Number: 1 to 65535 -->
    <!-- Mandatory -->
    <P27010>443</P27010>

    <!-- Web Access Mode. 0 - HTTPS, 1 - HTTP -->
    <!-- Number: 0, 1 -->
    <!-- Mandatory -->
    <P1650>1</P1650>

    <!-- Disable SSH. 0 - No, 1 - Yes -->
    <!-- Number: 0,1 -->
    <!-- Mandatory -->
    <P276>1</P276>

    <!-- Lockout time interval. minimum - 1 minute, maximum - 15 minutes -->
    <!-- Mandatory -->
    <P1683>15</P1683>

    <!-- Disable User Level Web Access. 0 - No, 1 - Yes -->
    <!-- Number: 0, 1 -->
    <!-- Mandatory -->
    <P28158>0</P28158>

    <!-- Disable Viewer Level Web Access. 0 - No, 1 - Yes -->
    <!-- Number: 0, 1 -->
    <!-- Mandatory -->
    <P28159>0</P28159>

    <!-- User Password -->
    <!-- P196=123 -->
    {% if user_password -%}
    <P196>{{ user_password }}</P196>
    {% endif -%}


    <!-- Admin password -->
    <!-- String Max Length: 30; between ascii values 33 and 126 -->
    <!-- Mandatory -->
    <!-- P2=admin -->
    {% if admin_password -%}
    <P2>{{ admin_password }}</P2>
    {% endif -%}
    
    <!-- White list for WAN side -->
    <!-- String: ip address -->
    <!-- <P20701></P20701> -->

    <!-- Black list for WAN side -->
    <!-- String: ip address -->
    <!-- <P20702></P20702> -->

    {% if ntp_enabled -%}
    <!-- NTP Server -->
    <!-- String: serveraddress -->
    <P30>{{ ntp_ip }}</P30>
    {% endif -%}
    {% if XX_timezone -%}
    <!-- Time Zone. Offset in minutes to GMT -->
    <!-- <value="TZA+12"> GMT-12:00 </option> -->
    <!-- <value="TZB+11"> GMT-11:00 </option> -->
    <!-- <value="TZC+10"> GMT-10:00 </option> -->
    <!-- <value="TZD+9"> GMT-09:00 </option> -->
    <!-- <value="TZE+8"> GMT-08:00 </option> -->
    <!-- <value="TZF+7"> GMT-07:00 </option> -->
    <!-- <value="TZG+6"> GMT-06:00 </option> -->
    <!-- <value="TZH+5"> GMT-05:00 </option> -->
    <!-- <value="TZf+4:30"> GMT-04:30 </option> -->
    <!-- <value="TZI+4"> GMT-04:00 </option> -->
    <!-- <value="TZJ+3:30"> GMT-03:30 </option> -->
    <!-- <value="TZK+3"> GMT-03:00 </option> -->
    <!-- <value="TZL+2"> GMT-02:00 </option> -->
    <!-- <value="TZM+1"> GMT-01:00 </option> -->
    <!-- <value="TZN+0"> GMT </option> -->
    <!-- <value="TZO-1"> GMT+01:00 </option> -->
    <!-- <value="TZP-2"> GMT+02:00 </option> -->
    <!-- <value="TZQ-3"> GMT+03:00 </option> -->
    <!-- <value="TZR-4"> GMT+04:00 </option> -->
    <!-- <value="TZS-5"> GMT+05:00 </option> -->
    <!-- <value="TZT-5:30"> GMT+05:30 </option> -->
    <!-- <value="TZU-5:45"> GMT+05:45 </option> -->
    <!-- <value="TZV-6"> GMT+06:00 </option> -->
    <!-- <value="TZW-6:30"> GMT+06:30 </option> -->
    <!-- <value="TZX-7"> GMT+07:00 </option> -->
    <!-- <value="TZY-8"> GMT+08:00 </option> -->
    <!-- <value="TZZ-9"> GMT+09:00 </option> -->
    <!-- <value="TZa-9:30"> GMT+09:30 </option> -->
    <!-- <value="TZb-10"> GMT+10:00 </option> -->
    <!-- <value="TZc-11"> GMT+11:00 </option> -->
    <!-- <value="TZd-12"> GMT+12:00 </option> -->
    <!-- <value="TZe-13"> GMT+13:00 </option> -->
    <!-- <value="customize"> Self-Defined Time Zone </option> -->
    <!-- Mandatory Category: string Max Length: 9 Range0: Min=a Max=z Range1: Min=A Max=Z Range2: Min=+ Max=: -->
    <P64>{{ XX_timezone }}</P64>
    {% endif -%}
    {% if XX_locale -%}
    <!-- LCD Display Language. en - English, zh - Chinese, fr - French, es - Spanish -->
    <!-- String -->
    <!-- Mandatory -->
    <P1362>{{ XX_locale }}</P1362>
    {% endif -%}
    {% if vlan_enabled -%}
    <!-- Layer 2 QoS 802.1Q/VLAN Tag for Service Interface -->
    <!-- Number -->
    <!-- Mandatory -->
    <P51>{{ vlan_id }}</P51>
    
    <!-- Layer 2 QoS 802.1Q/VLAN Tag for Management Interface. -->
    <!-- Number -->
    <P22111>{{ vlan_id }}</P22111>
    {% endif -%}

    {% if vlan_priority is defined -%}
    <!-- Layer 2 QoS 802.1p Priority Value for SIP signaling -->
    <!-- Number: 0 to 7 -->
    <!-- Mandatory -->
    <P5038>{{ vlan_priority }}</P5038>

    <!-- Layer 2 QoS 802.1p Priority Value for RTP media -->
    <!-- Number: 0 to 7 -->
    <!-- Mandatory -->
    <P5042>{{ vlan_priority }}</P5042>

    <!-- Layer 2 QoS 802.1p Priority Value for Management Interface. -->
    <!-- Number -->
    <P22112>0</P22112>
    {% endif -%}

    <!-- Unregister On Reboot. 0 - no, 1 - yes -->
    <!-- Number: 0,1 -->
    <!-- Mandatory -->
    <P81>1</P81>

    <!-- Profile 1-General Settings -->

    <!-- Profile Active.  0 - no, 1 - yes -->
    <!-- Number: 0,1 -->
    <!-- Mandatory -->
    <P271>1</P271>

    <!-- Primary SIP Server -->
    <!-- String: serveraddress -->
    <P47>{{ XX_main_proxy_ip }}</P47>

    <!-- Failover SIP Server -->
    <!-- String: serveraddress -->
    <!-- <P967></P967> -->

    <!-- Prefer Primary SIP Server. 0 - No, 1 - Yes. -->
    <!-- Number: 0,1 -->
    <!-- Mandatory -->
    <P4567>1</P4567>

    <!-- Primary Outbound Proxy -->
    <!-- String: serveraddress -->
    <P48>{{ XX_main_proxy_ip }}</P48>

    <!-- Backup Outbound Proxy. -->
    <!-- String: serveraddress -->
    <!-- <P2333></P2333> -->


    <!-- Prefer Primary Outbound Proxy. 0 - No, 1 - Yes -->
    <!-- Number: 0, 1 -->
    <!-- Mandatory -->
    <P28096>1</P28096>



{# SIP per-line settings -#}
    <!-- FXS Ports -->

    <!-- FXS Port -->
    <!-- SIP USER ID; String Max Length: 64 -->
    <!-- Authenticate ID; String Max Length: 64 -->
    <!-- Password; String Max Length: 64 -->
    <!-- Name; String Max Length: 64 -->
    <!-- Profile ID (0 - Profile 1, 1 - Profile 2, 2 - Profile 3, 3 - Profile 4); -->
    <!-- Enable FXS (TR-069) (0 - No, 1 - Yes, default is Yes) -->

    <!-- Offhook Auto-dial; String Max Length: 64 0 to 9,#,* -->
    <!-- Hunting Group (0 - None, 1 - Active, 2~32 - hunting group number 2~32) -->
    <!-- Request URI Routing ID -->

    <!-- Map to FXO Port -->
    <!-- Map to FXO Gateway IP -->
    <!-- Map to FXO Gateway Port -->

{% for line_no, line in sip_lines.iteritems() %}
  {% if line_no|int <= 30 %}
    {% set ref = line_no|int - 1 %}
    <!-- FXS {{ line_no }}  -->
    <P{{ 4060 + ref }}>{{ line['auth_username'] }}</P{{ 4060 + ref }}>
    <P{{ 4090 + ref }}>{{ line['auth_username'] }}</P{{ 4090 + ref }}>
    <P{{ 4120 + ref }}>{{ line['password'] }}</P{{ 4120 + ref }}>
    {% if line_no|int <= 20 %}
    <P{{ 4180 + ref }}>{{ line['display_name'] }}</P{{ 4180 + ref }}>
    {% else -%}
    <P{{ 4252 + ref - 20 }}>{{ line['display_name'] }}</P{{ 4252 + ref - 20 }}>
    {% endif -%}
    <P{{ 4150 + ref }}>0</P{{ 4150 + ref }}>
    <P{{ 4595 + ref }}>1</P{{ 4595 + ref }}>

    <!-- <P{{ 4210 + ref }}></P{{ 4210 + ref }}> -->
    <P{{ 4300 + ref }}>0</P{{ 4300 + ref }}>
    <!-- <P{{ 4669 + ref }}></P{{ 4669 + ref }}> -->

    <P{{ 4521 + ref }}>1</P{{ 4521 + ref }}>
    <!-- <P{{ 4264 + ref }}></P{{ 4264 + ref }}> -->
    <P{{ 4858 + ref }}>5060</P{{ 4858 + ref }}>
  {% else -%}
    {% if line_no|int <= 32 %}
      {% set ref = line_no|int - 31 %}
      <!-- FXS {{ line_no }}  -->
      <P{{ 4240 + ref }}>{{ line['auth_username'] }}</P{{ 4240 + ref }}>
      <P{{ 4242 + ref }}>{{ line['auth_username'] }}</P{{ 4242 + ref }}>
      <P{{ 4244 + ref }}>{{ line['password'] }}</P{{ 4244 + ref }}>
      <P{{ 4262 + ref }}>{{ line['display_name'] }}</P{{ 4262 + ref }}>
      <P{{ 4246 + ref }}>0</P{{ 4246 + ref }}>
      <P{{ 4625 + ref }}>1</P{{ 4625 + ref }}>

      <!-- <P{{ 4806 + ref }}></P{{ 4806 + ref }}> -->
      <P{{ 4250 + ref }}>0</P{{ 4250 + ref }}>
      <!-- <P{{ 4699 + ref }}></P{{ 4699 + ref }}> -->

      <P{{ 4809 + ref }}>1</P{{ 4809 + ref }}>
      <!-- <P{{ 4294 + ref }}></P{{ 4294 + ref }}> -->
      <P{{ 4888 + ref }}>5060</P{{ 4888 + ref }}>
    {% else -%}
      {% set ref = line_no|int - 33 %}
      <!-- FXS {{ line_no }}  -->
      <P{{ 21000 + ref }}>{{ line['auth_username'] }}</P{{ 21000 + ref }}>
      <P{{ 21064 + ref }}>{{ line['auth_username'] }}</P{{ 21064 + ref }}>
      <P{{ 21128 + ref }}>{{ line['password'] }}</P{{ 21128 + ref }}>
      <P{{ 21192 + ref }}>{{ line['display_name'] }}</P{{ 21192 + ref }}>
      <P{{ 21256 + ref }}>0</P{{ 21256 + ref }}>
      <P{{ 21384 + ref }}>1</P{{ 21384 + ref }}>

      <!-- <P{{ 21448 + ref }}></P{{ 21448 + ref }}> -->
      <P{{ 21320 + ref }}>0</P{{ 21320 + ref }}>
      <!-- <P{{ 21704 + ref }}></P{{ 21704 + ref }}> -->

      <P{{ 21512 + ref }}>1</P{{ 21512 + ref }}>
      <!-- <P{{ 21576 + ref }}></P{{ 21576 + ref }}> -->
      <P{{ 21640 + ref }}>5060</P{{ 21640 + ref }}>

    {% endif -%}
  {% endif -%}
{% endfor %}
{{ XX_fkeys }}
</config>
</gs_provision>


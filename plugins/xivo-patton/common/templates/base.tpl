cli version 3.20

{% if XX_timezone_offset -%}
clock local default-offset {{ XX_timezone_offset }}
{%- endif %}
{% if XX_dst_offset -%}
clock local dst-rule DSTRULE {{ XX_dst_offset }} from {{ XX_dst_start }} until {{ XX_dst_end }}
{%- endif %}

timer PROVISIONING_CONFIG now + 1 minute "provisioning execute PF_PROVISIONING_CONFIG"
timer PROVISIONING_FIRMWARE now + 1 minute "provisioning execute PF_PROVISIONING_FIRMWARE"

{% if ntp_enabled -%}
sntp-client
sntp-client server primary {{ ntp_ip }}
{%- endif %}

{% if admin_password -%}
administrator {{ admin_username|d('administrator') }} password {{ admin_password }}
{%- endif %}
{% if user_username and user_password -%}
operator {{ user_username }} password {{ user_password }}
{%- endif %}

profile provisioning PF_PROVISIONING_CONFIG
  destination configuration
  location 1 $(dhcp.66)/$(system.mac).cfg
  activation reload graceful

actions
  rule ACT_CHECK_SYNC
    condition sip gateway:GW_SIP NOTIFY_CHECK_SYNC_RELOAD
    action "provisioning execute PF_PROVISIONING_CONFIG"

{% if syslog_enabled -%}
syslog-client
  remote {{ syslog_ip }} {{ syslog_port }}
    facility kernel severity informational
    facility sip severity {{ XX_syslog_level }}
{%- endif %}

system
  ic voice 0
    low-bitrate-codec g729

{% include 'region_FR.tpl' %}

context ip router
  interface eth0
    ipaddress dhcp
    tcp adjust-mss rx mtu
    tcp adjust-mss tx mtu

{% if vlan_enabled and vlan_priority is defined -%}
profile service-policy SP_VLAN_PRIO
  source traffic-class default
    set layer2 cos {{ vlan_priority }}

context ip router
  interface eth0
    use profile service-policy SP_VLAN_PRIO out
{%- endif %}

port ethernet 0 0
  medium auto
  {% if vlan_enabled -%}
  vlan {{ vlan_id }}
    encapsulation ip
    bind interface eth0 router
    no shutdown
  {%- else -%}
  encapsulation ip
  bind interface eth0 router
  {%- endif %}

port ethernet 0 0
  no shutdown

context cs switch
  routing-table called-uri RT_FROM_SIP
    {% for line in XX_lines -%}
    route sip:{{ line['username'] }}@.% dest-interface IF_FXS{{ line['fxs_port_no'] }}
    {% endfor %}

  {% for server in XX_servers -%}
  interface sip IF_SIP_SERVER{{ server['id'] }}
    bind context sip-gateway GW_SIP
    route call dest-table RT_FROM_SIP
    remote {{ server['proxy_ip'] }} {{ server['proxy_port'] }}
  {% endfor %}

  {% for line in XX_lines -%}
  service hunt-group HG_FROM_FXS{{ line['fxs_port_no'] }}
    timeout 3
    {% for server in line['servers'] -%}
    route call dest-interface IF_SIP_SERVER{{ server['id'] }}
    {% endfor %}

  routing-table called-e164 RT_FROM_FXS{{ line['fxs_port_no'] }}
    route .T dest-service HG_FROM_FXS{{ line['fxs_port_no'] }}

  interface fxs IF_FXS{{ line['fxs_port_no'] }}
    route call dest-table RT_FROM_FXS{{ line['fxs_port_no'] }}
    message-waiting-indication stutter-dial-tone
    message-waiting-indication frequency-shift-keying
    call-transfer
    subscriber-number {{ line['username'] }}

  {% endfor %}

context cs switch
  no shutdown

authentication-service AUTH
  {% for line in XX_lines -%}
  username {{ line['auth_username'] }} password {{ line['password'] }}
  {% endfor %}

{% for server in XX_servers -%}
location-service LOC_SERVER{{ server['id'] }}
  domain {{ server['proxy_ip'] }}

  {% for line in server['lines'] -%}
  identity {{ line['username'] }}
    authentication outbound
      authenticate authentication-service AUTH username {{ line['auth_username'] }}
    call outbound
      preferred-transport-protocol {{ sip_transport }}
    message inbound
      subscribe implicit
    registration outbound
      register auto
      {% if server['proxy_ip'] == line['proxy_ip'] -%}
      registrar {{ line['registrar_ip'] }} {{ line['registrar_port'] }}
      {%- else -%}
      registrar {{ line['backup_registrar_ip'] }} {{ line['backup_registrar_port'] }}
      {%- endif %}
      preferred-transport-protocol {{ sip_transport }}
  {% endfor %}
{% endfor %}

context sip-gateway GW_SIP
  interface TRANSPORT_ETH0
    bind interface eth0 port 5060

context sip-gateway GW_SIP
  {% for server in XX_servers -%}
  bind location-service LOC_SERVER{{ server['id'] }}
  {% endfor %}
  notify check-sync accept
  no shutdown

{% for line in XX_lines -%}
port fxs 0 {{ line['fxs_port_no'] }}
  encapsulation cc-fxs
  bind interface IF_FXS{{ line['fxs_port_no'] }} switch
  no shutdown
{% endfor %}


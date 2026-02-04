#!version:1.0.0.1

static.auto_provision.server.url = {{ XX_server_url }}/
static.firmware.url = {{ XX_server_url }}/firmware/{{ XX_fw_filename }}

{% if XX_handsets_fw -%}
{% for handset, fw_file in XX_handsets_fw.items() -%}
over_the_air.url.{{ handset }} = {{ XX_server_url }}/firmware/{{ fw_file }}
{% endfor -%}
over_the_air.handset_tip = 0
{%- endif %}

static.auto_provision.pnp_enable = 0
static.auto_provision.custom.protect = 1

distinctive_ring_tones.alert_info.1.text = ring1
distinctive_ring_tones.alert_info.2.text = ring2
distinctive_ring_tones.alert_info.3.text = ring3
distinctive_ring_tones.alert_info.4.text = ring4
distinctive_ring_tones.alert_info.5.text = ring5
distinctive_ring_tones.alert_info.6.text = ring6
distinctive_ring_tones.alert_info.7.text = ring7
distinctive_ring_tones.alert_info.8.text = ring8
distinctive_ring_tones.alert_info.1.ringer = 1
distinctive_ring_tones.alert_info.2.ringer = 2
distinctive_ring_tones.alert_info.3.ringer = 3
distinctive_ring_tones.alert_info.4.ringer = 4
distinctive_ring_tones.alert_info.5.ringer = 5
distinctive_ring_tones.alert_info.6.ringer = 6
distinctive_ring_tones.alert_info.7.ringer = 7
distinctive_ring_tones.alert_info.8.ringer = 8

features.caller_name_type_on_dialing = 1
features.text_message.enable = 0
features.text_message_popup.enable = 0
features.config_dsskey_length = 1
features.dnd.large_icon.enable = 1
{% for line_no, line in XX_sip_lines.items() if line -%}
features.action_uri_limit_ip = {{ line['proxy_ip'] }}
{% endfor -%}
features.show_action_uri_option = 0

local_time.date_format = {{ XX_handset_lang|d('2') }}

sip.notify_reboot_enable = 0
sip.trust_ctrl = 1
features.direct_ip_call_enable = 1

transfer.dsskey_deal_type = 1

{% if vlan_enabled -%}
static.network.vlan.internet_port_enable = 1
static.network.vlan.internet_port_vid = {{ vlan_id }}
static.network.vlan.internet_port_priority = {{ vlan_priority|d('%NULL%') }}
{% else -%}
static.network.vlan.internet_port_enable = 0
static.network.vlan.internet_port_vid = %NULL%
static.network.vlan.internet_port_priority = %NULL%
{% endif %}

{% if vlan_enabled and vlan_pc_port_id -%}
static.network.vlan.pc_port_enable = 1
static.network.vlan.pc_port_vid = {{ vlan_pc_port_id }}
{% else -%}
static.network.vlan.pc_port_enable = 0
static.network.vlan.pc_port_vid = %NULL%
{% endif %}

{% if syslog_enabled -%}
static.syslog.enable = 1
static.syslog.server = {{ syslog_ip }}
{% else -%}
static.syslog.enable = 0
static.syslog.server = %NULL%
{% endif %}

lang.wui = {{ XX_lang|d('%NULL%') }}
lang.gui = {{ XX_lang|d('%NULL%') }}

voice.tone.country = {{ XX_country|d('%NULL%') }}

local_time.ntp_server1 = {{ ntp_ip|d('pool.ntp.org') }}
{% if XX_timezone -%}
{{ XX_timezone }}
{% else -%}
local_time.time_zone = %NULL%
local_time.time_zone_name = %NULL%
local_time.summer_time = %NULL%
{% endif %}

{% if XX_xivo_phonebook_url -%}
remote_phonebook.data.1.url = {{ XX_xivo_phonebook_url }}
remote_phonebook.data.1.name = Wazo
{% else -%}
remote_phonebook.data.1.url = %NULL%
remote_phonebook.data.1.name = %NULL%
{% endif %}

static.security.user_name.user = {{ user_username|d('user') }}
static.security.user_name.admin = {{ admin_username|d('admin') }}
static.security.user_password = {{ user_username|d('user') }}:{{ user_password|d('user') }}
static.security.user_password = {{ admin_username|d('admin') }}:{{ admin_password|d('admin') }}

static.usb.power.enable = 1

{% for line_no, line in XX_sip_lines.items() -%}
{% if line -%}
account.{{ line_no }}.enable = 1
account.{{ line_no }}.label = {{ line['display_name'] }}
account.{{ line_no }}.auth_name = {{ line['auth_username'] }}
account.{{ line_no }}.user_name = {{ line['username'] }}
account.{{ line_no }}.password = {{ line['password'] }}
account.{{ line_no }}.sip_server.1.address = {{ line['proxy_ip'] }}
account.{{ line_no }}.sip_server.1.port = {{ line['proxy_port']|d('%NULL%') }}
account.{{ line_no }}.sip_server.1.transport_type = {{ XX_sip_transport }}
account.{{ line_no }}.sip_server.2.address = {{ line['backup_proxy_ip']|d('%NULL%') }}
account.{{ line_no }}.sip_server.2.port = {{ line['backup_proxy_port']|d('%NULL%') }}
account.{{ line_no }}.sip_server.2.transport_type = {{ XX_sip_transport }}
account.{{ line_no }}.fallback.redundancy_type = 1
account.{{ line_no }}.cid_source = 2
account.{{ line_no }}.alert_info_url_enable = 0
account.{{ line_no }}.nat.udp_update_enable = 1
account.{{ line_no }}.dtmf.type = {{ line['XX_dtmf_type']|d('2') }}
account.{{ line_no }}.dtmf.info_type = 1
{% if XX_sip_transport == '2' and line['number'] != 'autoprov' -%}
account.{{ line_no }}.srtp_encryption = 2
{% else -%}
account.{{ line_no }}.srtp_encryption = 0
{% endif %}

account.{{ line_no }}.codec.g722.enable = 1
account.{{ line_no }}.codec.g722_1c_48kpbs.enable = 1
account.{{ line_no }}.codec.g722_1c_32kpbs.enable = 1
account.{{ line_no }}.codec.g722_1c_24kpbs.enable = 1
account.{{ line_no }}.codec.g722_1_24kpbs.enable = 1
account.{{ line_no }}.codec.pcmu.enable = 1
account.{{ line_no }}.codec.pcma.enable = 1
account.{{ line_no }}.codec.g729.enable = 1
account.{{ line_no }}.codec.g726_16.enable = 0
account.{{ line_no }}.codec.g726_24.enable = 0
account.{{ line_no }}.codec.g726_32.enable = 0
account.{{ line_no }}.codec.g726_40.enable = 0
account.{{ line_no }}.codec.g723_53.enable = 0
account.{{ line_no }}.codec.g723_63.enable = 0
account.{{ line_no }}.codec.opus.enable = 0
account.{{ line_no }}.codec.ilbc.enable = 0

{% if sip_subscribe_mwi -%}
account.{{ line_no }}.subscribe_mwi = 1
{% endif %}
voice_mail.number.{{ line_no }} = {{ line['voicemail']|d('%NULL%') }}
{% else -%}
account.{{ line_no }}.enable = 0
account.{{ line_no }}.label = %NULL%
account.{{ line_no }}.display_name = %NULL%
account.{{ line_no }}.auth_name = %NULL%
account.{{ line_no }}.user_name = %NULL%
account.{{ line_no }}.password = %NULL%
account.{{ line_no }}.sip_server.1.address = %NULL%
account.{{ line_no }}.sip_server.1.port = %NULL%
account.{{ line_no }}.sip_server.1.transport_type = %NULL%
account.{{ line_no }}.sip_server.2.address = %NULL%
account.{{ line_no }}.sip_server.2.port = %NULL%
account.{{ line_no }}.sip_server.2.transport_type = %NULL%
account.{{ line_no }}.subscribe_mwi = %NULL%
voice_mail.number.{{ line_no }} = %NULL%
{% endif %}
{% endfor %}

{% if XX_options['switchboard'] -%}
call_waiting.enable = 0
{% else -%}
call_waiting.enable = 1
{% endif %}

static.directory_setting.url = {{ XX_server_url }}/directory_setting.xml

{% if XX_wazo_phoned_user_service_dnd_enabled_url -%}
action_url.dnd_on = {{ XX_wazo_phoned_user_service_dnd_enabled_url }}
{% endif -%}
{% if XX_wazo_phoned_user_service_dnd_disabled_url -%}
action_url.dnd_off = {{ XX_wazo_phoned_user_service_dnd_disabled_url }}
{% endif -%}

{{ XX_fkeys }}

#######################################################################################
##                                    Network CDP                                    ##
#######################################################################################
static.network.cdp.enable =
static.network.cdp.packet_interval =



#######################################################################################
##                                    Network IPv6                                   ##
#######################################################################################
static.network.ipv6_static_dns_enable =
static.network.ipv6_icmp_v6.enable =
static.network.ipv6_secondary_dns =
static.network.ipv6_primary_dns =
static.network.ipv6_internet_port.gateway =
static.network.ipv6_internet_port.ip =
static.network.ipv6_internet_port.type =
static.network.ipv6_prefix =



#######################################################################################
##                                    Network WiFi                                   ##
#######################################################################################

##static.wifi.X.ssid=
##static.wifi.X.priority=
##static.wifi.X.security_mode=
##static.wifi.X.password=
##static.wifi.X.eap_type=
##static.wifi.X.eap_user_name=
##static.wifi.x.eap_password=
##(X ranges from 1 to 5)
##Only T5XW/T54S/T52S/T48G/T48S/T46G/T46S/T42S/T41S/T29G/T27G/T4XU Models support these parameters.

static.wifi.enable =
static.wifi.1.label =
static.wifi.1.ssid =
static.wifi.1.priority =
static.wifi.1.security_mode =
static.wifi.1.cipher_type =
static.wifi.1.password =
static.wifi.1.eap_type =
static.wifi.1.eap_user_name =
static.wifi.1.eap_password =
static.wifi.show_scan_prompt =

##V83 Add
static.wifi.function.enable =


##V84 SP4 ADD
static.network.wifi.ip_address_mode=
static.network.wifi.preference =
static.network.wifi.internet_port.type =
static.network.wifi.internet_port.ip=
static.network.wifi.internet_port.mask=
static.network.wifi.internet_port.gateway=
static.network.wifi.static_dns_enable=
static.network.wifi.primary_dns=
static.network.wifi.secondary_dns=
static.network.wifi.ipv6_internet_port.type=
static.network.wifi.ipv6_internet_port.ip=
static.network.wifi.ipv6_prefix=
static.network.wifi.ipv6_internet_port.gateway=
static.network.wifi.ipv6_static_dns_enable=
static.network.wifi.ipv6_primary_dns=
static.network.wifi.ipv6_secondary_dns=
static.network.wifi.ipv6_icmp_v6.enable=


#######################################################################################
##                                 Network Internet                                  ##
#######################################################################################
static.network.ip_address_mode =
static.network.span_to_pc_port =
static.network.static_dns_enable =
static.network.pc_port.enable =
static.network.primary_dns =
static.network.secondary_dns =
static.network.internet_port.gateway =
static.network.internet_port.mask =
static.network.internet_port.ip =
static.network.internet_port.type =

##V83 Add
static.network.preference =


#######################################################################################
##                               Network Advanced                                    ##
#######################################################################################
static.network.dhcp_host_name =
static.network.dhcp.option60type =
static.network.mtu_value =
static.network.qos.audiotos =
static.network.port.min_rtpport =
static.network.port.max_rtpport =
static.network.qos.signaltos =

static.wui.http_enable =
static.wui.https_enable =
static.network.port.https =
static.network.port.http =

static.network.pc_port.speed_duplex =
static.network.internet_port.speed_duplex =

##V83 Add
static.network.redundancy.mode =
static.network.redundancy.failback.timeout =



#######################################################################################
##                                   Network LLDP                                    ##
#######################################################################################
static.network.lldp.enable =
static.network.lldp.packet_interval =


#######################################################################################
##                                    Network VPN                                    ##
#######################################################################################
static.network.vpn_enable =
static.openvpn.url =



#######################################################################################
##                                 Network 802.1x                                    ##
#######################################################################################
static.network.802_1x.mode =
static.network.802_1x.identity =
static.network.802_1x.md5_password =
static.network.802_1x.client_cert_url =
static.network.802_1x.root_cert_url =
static.network.802_1x.eap_fast_provision_mode =
static.network.802_1x.anonymous_identity =
static.network.802_1x.proxy_eap_logoff.enable =


static.auto_provision.custom.sync =
static.auto_provision.custom.sync.path =
static.auto_provision.custom.upload_method =




#######################################################################################
##                                    ZERO Touch                                     ##
#######################################################################################
static.zero_touch.enable =
static.zero_touch.wait_time =
static.features.hide_zero_touch_url.enable =
static.zero_touch.network_fail_delay_times =
static.zero_touch.network_fail_wait_times =


#######################################################################################
##                                   Autop URL                                       ##
#######################################################################################
static.auto_provision.server.username =
static.auto_provision.server.password =


#######################################################################################
##                                   Autop Weekly                                    ##
#######################################################################################
static.auto_provision.weekly.enable =
static.auto_provision.weekly.dayofweek =
static.auto_provision.weekly.end_time =
static.auto_provision.weekly.begin_time =
static.auto_provision.weekly_upgrade_interval =

#######################################################################################
##                                   Autop Repeat                                    ##
#######################################################################################
static.auto_provision.repeat.enable =
static.auto_provision.repeat.minutes =

#######################################################################################
##                                   Autop DHCP                                      ##
#######################################################################################
static.auto_provision.dhcp_option.list_user_options =
static.auto_provision.dhcp_option.enable =

##V83 Add
static.auto_provision.dhcp_option.list_user6_options =

#######################################################################################
##                                   Autop Mode                                      ##
#######################################################################################
static.auto_provision.power_on =



#######################################################################################
##                               Flexible Autop                                      ##
#######################################################################################
static.auto_provision.flexible.end_time =
static.auto_provision.flexible.begin_time =
static.auto_provision.flexible.interval =
static.auto_provision.flexible.enable =

#######################################################################################
##                                 Autoprovision  Other                              ##
#######################################################################################
static.auto_provision.prompt.enable =
static.auto_provision.attempt_expired_time =
static.auto_provision.attempt_before_failed =
static.network.attempt_expired_time =
static.auto_provision.update_file_mode =
static.auto_provision.retry_delay_after_file_transfer_failed=
static.auto_provision.inactivity_time_expire =
static.auto_provision.dns_resolv_timeout =
static.auto_provision.dns_resolv_nretry =
static.auto_provision.dns_resolv_nosys =
static.auto_provision.user_agent_mac.enable =
static.auto_provision.server.type =
features.action_uri_force_autop =
static.auto_provision.url_wildcard.pn =
static.auto_provision.reboot_force.enable =
static.auto_provision.dhcp_option.option60_value =
static.custom_mac_cfg.url =
static.auto_provision.aes_key_in_file =
features.custom_version_info =
##V83 Add
static.auto_provision.authentication.expired_time =
static.auto_provision.connect.keep_alive =

##V84 Add
static.auto_provision.config_version.mac=
static.auto_provision.config_version.com=


#######################################################################################
##                                   Autop Code                                      ##
#######################################################################################
##static.autoprovision.X.name
##static.autoprovision.X.code
##static.autoprovision.X.url
##static.autoprovision.X.user
##static.autoprovision.X.password
##static.autoprovision.X.com_aes
##static.autoprovision.X.mac_aes
##Autop Code(X ranges from 1 to 50)

static.autoprovision.1.name =
static.autoprovision.1.code =
static.autoprovision.1.url =
static.autoprovision.1.user =
static.autoprovision.1.password =
static.autoprovision.1.com_aes =
static.autoprovision.1.mac_aes =



#######################################################################################
##                                   TR069                                           ##
#######################################################################################

static.managementserver.enable =
static.managementserver.username =
static.managementserver.password =
static.managementserver.url =
static.managementserver.periodic_inform_enable =
static.managementserver.periodic_inform_interval =
static.managementserver.connection_request_password =
static.managementserver.connection_request_username =



#######################################################################################
##                            Confguration                                           ##
#######################################################################################
features.reset_by_long_press_enable =
features.factory_pwd_enable =
static.configuration.url =
static.features.custom_factory_config.enable =
static.custom_factory_configuration.url =


#######################################################################################
##                               SYSLOG                                              ##
#######################################################################################
static.syslog.level =
static.syslog.server_port =
static.syslog.transport_type =
static.syslog.facility =
static.syslog.prepend_mac_address.enable =
static.local_log.enable =
static.local_log.level =
static.local_log.max_file_size =



#######################################################################################
##                               Log Backup                                          ##
#######################################################################################
static.auto_provision.local_log.backup.enable =
static.auto_provision.local_log.backup.path =
static.auto_provision.local_log.backup.upload_period =
static.auto_provision.local_log.backup.append =
static.auto_provision.local_log.backup.bootlog.upload_wait_time=
static.auto_provision.local_log.backup.append.max_file_size =
static.auto_provision.local_log.backup.append.limit_mode=



#######################################################################################
##                                   User Mode                                       ##
#######################################################################################
static.security.var_enable =
static.web_item_level.url =


#######################################################################################
##                                  Quick Login                                      ##
#######################################################################################
wui.quick_login =


#######################################################################################
##                               Security                                            ##
#######################################################################################
static.phone_setting.reserve_certs_enable =
features.relog_offtime =
static.security.default_ssl_method =
static.security.cn_validation =
static.security.dev_cert =
static.security.ca_cert =
static.security.trust_certificates =
static.security.user_name.var =

##V83 Add
static.security.default_access_level =
phone_setting.reserve_certs_config.enable =


#######################################################################################
##                               Watch Dog                                           ##
#######################################################################################
static.watch_dog.enable =

#######################################################################################
##                                   Server Certificates                             ##
#######################################################################################
static.server_certificates.url =
static.server_certificates.delete =

#######################################################################################
##                           Trusted Certificates                                    ##
#######################################################################################
static.trusted_certificates.url =
static.trusted_certificates.delete =



#######################################################################################
##                           Secure Domain List                                      ##
#######################################################################################
wui.secure_domain_list =


#######################################################################################
##                               Encryption                                          ##
#######################################################################################
static.auto_provision.encryption.directory =
static.auto_provision.encryption.call_log =
static.auto_provision.encryption.config =




#######################################################################################
##                                   Trnasfer                                        ##
#######################################################################################
dialplan.transfer.mode =
transfer.on_hook_trans_enable =
transfer.tran_others_after_conf_enable =
transfer.blind_tran_on_hook_enable =
transfer.semi_attend_tran_enable =
phone_setting.call_appearance.transfer_via_new_linekey=


#######################################################################################
##                                   Conference                                      ##
#######################################################################################
features.conference.with_previous_call.enable =
features.local_conf.combine_with_one_press.enable=
phone_setting.call_appearance.conference_via_new_linekey=



#######################################################################################
##                                   Anonymous                                       ##
#######################################################################################
features.anonymous_response_code=



#######################################################################################
##                          Call Configuration                                       ##
#######################################################################################
phone_setting.incoming_call_when_dialing.priority=
phone_setting.hold_or_swap.mode=
features.play_held_tone.interval=
features.play_held_tone.delay=
features.play_held_tone.enable=
features.play_hold_tone.interval=
features.ignore_incoming_call.enable=
force.voice.ring_vol=
features.mute.autoanswer_mute.enable=
features.play_hold_tone.delay =
phone_setting.end_call_net_disconnect.enable =
features.custom_auto_answer_tone.enable=
default_input_method.dialing=
features.speaker_mode.enable=
features.headset_mode.enable=
features.handset_mode.enable=
features.conference.local.enable =
features.off_hook_answer.enable=
phone_setting.show_code403=
phone_setting.ring_for_tranfailed=
features.password_dial.length=
features.password_dial.prefix=
features.password_dial.enable=
features.group_listen_in_talking_enable=
phone_setting.call_info_display_method=
phone_setting.called_party_info_display.enable =
features.headset_training=
features.headset_prior=
features.dtmf.replace_tran =
features.dtmf.transfer =
phone_setting.ringing_timeout=
phone_setting.ringback_timeout=

features.keep_mute.enable=
linekey.1.shortlabel=
features.config_dsskey_length.shorten =
features.auto_linekeys.enable=
phone_setting.call_appearance.calls_per_linekey=
features.linekey_call_with_default_account=
##V83 Add
features.station_name.value =
features.station_name.scrolling_display =
voice.headset.autoreset_spk_vol =
voice.handset.autoreset_spk_vol =
voice.handfree.autoreset_spk_vol =
features.headset.ctrl_call.enable =
phone_setting.incoming_call.reject.enable =

features.play_mute_tone.enable=
features.play_mute_tone.interval=

features.call_out_directory_by_off_hook.enable=
features.congestion_tone.codelist=


##V84 Add
phone_setting.icon.delete=
phone_setting.icon.url=

##V84 SP4 Add
voice.handset.tia4965.enable =
voice.headset.tia4965.enable =

#######################################################################################
##                           Custom Softkey                                          ##
#######################################################################################
phone_setting.custom_softkey_enable=
custom_softkey_talking.url=
custom_softkey_ring_back.url=
custom_softkey_dialing.url=
custom_softkey_connecting.url=
custom_softkey_call_in.url=
custom_softkey_call_failed.url=

##V83 Add
features.homescreen_softkey.acd.enable =
features.homescreen_softkey.hoteling.enable =
phone_setting.custom_softkey.apply_to_states =
features.custom_softkey_dynamic.enable =


#######################################################################################
##                                   Features Bluetooth                              ##
#######################################################################################
##Only T5XW/T54S/T52S/T48G/T48S/T46G/T46S/T42S/T41S/T29G/T27G/T4XU Models support the parameter.
features.bluetooth_enable=
features.bluetooth_adapter_name=
##V83 Add
static.bluetooth.function.enable =

##V84 Add
bluetooth.a2dp_sink=
bluetooth.connect_confirm.enable=

#######################################################################################
##                                  Features USB Record                              ##
#######################################################################################
##Only T5XW/T54S/T52S/T48G/T48S/T46G/T46S/T42S/T41S/T29G/T27G/T4XU Models support the parameter.
features.usb_call_recording.enable =
features.auto_recording.enable =

features.idle_recording.enable=

#######################################################################################
##                                  Features USB                                     ##
#######################################################################################
##V84 Add
static.usbdisk.function.enable=

#######################################################################################
##                                    Codec                                          ##
#######################################################################################
voice.g726.aal2.enable=


#######################################################################################
##                                   DTMF                                            ##
#######################################################################################
features.dtmf.min_interval=
features.dtmf.volume=
features.dtmf.duration =

#######################################################################################
##                                   Tones                                           ##
#######################################################################################
voice.tone.autoanswer =
voice.tone.message =
voice.tone.stutter =
voice.tone.info =
voice.tone.dialrecall =
voice.tone.callwaiting =
voice.tone.congestion =
voice.tone.busy =
voice.tone.ring =
voice.tone.dial =
voice.side_tone =
features.partition_tone =
voice.tone.secondary_dial=
#######################################################################################
##  Tones≤π≥‰ºº ı÷ß≥÷º"V83÷––'µƒstutterdial"¶"√£¨–Ë≈‰∫œ"'œ¬dnd°¢fwd°¢vm≥°æ∞ π"√      ##
#######################################################################################

voice.tone.stutterdial=
voice.tone.stutter_dial_tone.apply_to_dnd.enable=
voice.tone.stutter_dial_tone.apply_to_fwd.enable=

#######################################################################################
##                                   Jitter Buffer                                   ##
#######################################################################################
voice.jib.normal=
voice.jib.max =
voice.jib.min =
voice.jib.adaptive =

voice.jib.wifi.normal=
voice.jib.wifi.max=
voice.jib.wifi.min=
voice.jib.wifi.adaptive=

#######################################################################################
##                                   Echo Cancellation                               ##
#######################################################################################
voice.echo_cancellation =
voice.cng =
voice.vad =

##V84 Add
voice.ans_nb.enable=
voice.tns.enable=

################################################################
#                        SIP Backup Server                    ##
################################################################
static.network.dns.ttl_enable =
static.network.dns.last_cache_expired.enable=
static.network.dns.last_cache_expired =
static.network.dns.query_timeout =
static.network.dns.retry_times =
sip.dns_transport_type=
sip.skip_redundant_failover_addr=


################################################################
#                        SIP Basic Config                     ##
################################################################
sip.use_out_bound_in_dialog=
sip.unreg_with_socket_close=
phone_setting.disable_account_without_username.enable=
features.auto_answer.first_call_only=

##V84 Add
phone_setting.call_display_name.mode=

################################################################
#                        SIP Advanced config                  ##
################################################################
sip.request_validation.event=
sip.sdp_early_answer_or_offer=
sip.cid_source.preference=
sip.request_validation.digest.realm=
sip.request_validation.digest.list=
sip.request_validation.source.list=
sip.send_keepalive_by_socket=
sip.reliable_protocol.timerae.enable=
sip.requesturi.e164.addglobalprefix=
sip.mac_in_ua=

sip.timer_t1=
sip.timer_t2=
sip.timer_t4=

sip.listen_mode=
sip.listen_port=
sip.tls_listen_port=
sip.tcp_port_random_mode=
sip.escape_characters.enable=
sip.send_response_by_request=
sip.disp_incall_to_info=
features.call_invite_format=
phone_setting.early_media.rtp_sniffer.timeout=
sip.reg_surge_prevention =

################################################################
#    V84 new add ≈‰∫œsip.escape_characters.enable= π"√        ##
################################################################
sip.reserve_characters=


##V83 Add
sip.dhcp.option120.mode =

################################################################
#                        NAT&ICE                              ##
################################################################
static.sip.nat_turn.enable=
static.sip.nat_turn.username=
static.sip.nat_turn.password=
static.sip.nat_turn.server=
static.sip.nat_turn.port=

static.sip.nat_stun.enable=
static.sip.nat_stun.server=
static.sip.nat_stun.port=


static.ice.enable=
static.network.static_nat.enable=
static.network.static_nat.addr=

#######################################################################################
##                           DNS                                                     ##
#######################################################################################
dns_cache_a.1.name =
dns_cache_a.1.ip =
dns_cache_a.1.ttl =
dns_cache_srv.1.name =
dns_cache_srv.1.port =
dns_cache_srv.1.priority =
dns_cache_srv.1.target =
dns_cache_srv.1.weight =
dns_cache_srv.1.ttl =
dns_cache_naptr.1.name =
dns_cache_naptr.1.order =
dns_cache_naptr.1.preference =
dns_cache_naptr.1.replace =
dns_cache_naptr.1.service =
dns_cache_naptr.1.ttl =

#######################################################################################
##                                 RTP                                               ##
#######################################################################################
features.rtp_symmetric.enable=


#######################################################################################
##                                 RTCP-XR                                           ##
#######################################################################################
voice.rtcp.enable=
voice.rtcp_cname=
voice.rtcp_xr.enable=
phone_setting.vq_rtcpxr_display_symm_oneway_delay.enable=
phone_setting.vq_rtcpxr_display_round_trip_delay.enable=
phone_setting.vq_rtcpxr_display_moscq.enable=
phone_setting.vq_rtcpxr_display_moslq.enable =
phone_setting.vq_rtcpxr_display_packets_lost.enable=
phone_setting.vq_rtcpxr_display_jitter_buffer_max.enable=
phone_setting.vq_rtcpxr_display_jitter.enable=
phone_setting.vq_rtcpxr_display_remote_codec.enable=
phone_setting.vq_rtcpxr_display_local_codec.enable=
phone_setting.vq_rtcpxr_display_remote_call_id.enable=
phone_setting.vq_rtcpxr_display_local_call_id.enable=
phone_setting.vq_rtcpxr_display_stop_time.enable=
phone_setting.vq_rtcpxr_display_start_time.enable=
phone_setting.vq_rtcpxr_interval_period=
phone_setting.vq_rtcpxr_delay_threshold_critical=
phone_setting.vq_rtcpxr_delay_threshold_warning=
phone_setting.vq_rtcpxr_moslq_threshold_critical=
phone_setting.vq_rtcpxr_moslq_threshold_warning=
phone_setting.vq_rtcpxr.interval_report.enable=
phone_setting.vq_rtcpxr.states_show_on_gui.enable=
phone_setting.vq_rtcpxr.states_show_on_web.enable=
phone_setting.vq_rtcpxr.session_report.enable=


#######################################################################################
##                                   Contact                                         ##
#######################################################################################
super_search.url=

local_contact.data.url=
local_contact.data.delete=

##Only T5XW/T54S/T52S/T48G/T48S/T46G/T46S/T29G/T46U/T48U Models support the parameter
phone_setting.contact_photo_display.enable=

phone_setting.incoming_call.horizontal_roll_interval=

##Only T5XW/T54S/T52S/T48G/T48S/T46G/T46S/T29G/T5XW Models support the parameter
local_contact.data_photo_tar.url=
local_contact.photo.url=
local_contact.image.url=

##Only T48G/S Models support the parameter
local_contact.icon_image.url=
local_contact.icon.url=

search_in_dialing.local_directory.enable =
search_in_dialing.local_directory.priority =

#######################################################################################
##                                 Remote Phonebook                                  ##
#######################################################################################
##remote_phonebook.data.X.url
##remote_phonebook.data.X.name
#remote_phonebook.data.X.username=
#remote_phonebook.data.X.password=
##(X ranges from 1 to 5)

features.remote_phonebook.enter_update_enable=
features.remote_phonebook.flash_time=
features.remote_phonebook.enable=
remote_phonebook.display_name=

directory_setting.remote_phone_book.enable =
directory_setting.remote_phone_book.priority =
search_in_dialing.remote_phone_book.enable =
search_in_dialing.remote_phone_book.priority =

##V84 ADD
remote_phonebook.data.1.username=
remote_phonebook.data.1.password=


#######################################################################################
##                                 LDAP                                              ##
#######################################################################################
ldap.enable=
ldap.user=
ldap.password=
ldap.base=
ldap.port=
ldap.host=
ldap.customize_label=
ldap.incoming_call_special_search.enable=
ldap.tls_mode=
ldap.search_type=
ldap.numb_display_mode=
ldap.ldap_sort=
ldap.call_in_lookup=
ldap.version =
ldap.display_name=
ldap.numb_attr=
ldap.name_attr=
ldap.max_hits=
ldap.number_filter=
ldap.name_filter=
ldap.call_out_lookup=
directory_setting.ldap.enable =
directory_setting.ldap.priority =
search_in_dialing.ldap.enable =
search_in_dialing.ldap.priority =

##V84 SP4 ADD
ldap.custom_extra_attr_name=
ldap.display_extra_attr=
ldap.extra_attr=




#######################################################################################
##                                 History                                           ##
#######################################################################################
static.auto_provision.local_calllog.write_delay.terminated=
static.auto_provision.local_calllog.backup.path=
static.auto_provision.local_calllog.backup.enable=
super_search.recent_call=
features.call_out_history_by_off_hook.enable=
features.save_call_history=
features.call_log_show_num=
search_in_dialing.history.enable=
search_in_dialing.history.priority=
directory_setting.history.enable=
directory_setting.history.priority =
features.save_init_num_to_history.enable=
features.redial_via_local_sip_server.enable=

##V83 Add
features.calllog_detailed_information =

##V84 Add
features.call_log_merge.enable=


#######################################################################################
##                          Contact Backup                                           ##
#######################################################################################
static.auto_provision.local_contact.backup.path =
static.auto_provision.local_contact.backup.enable=


#######################################################################################
##                          Contact Other                                            ##
#######################################################################################
directory.search_type=
directory_setting.local_directory.enable =
directory_setting.local_directory.priority =

##V83 Add
phone_setting.search.highlight_keywords.enable =

#######################################################################################
##                          Favorites                                                ##
#######################################################################################
##V83 Add
local_contact.favorite.enable =
phone_setting.favorite_sequence_type =

#######################################################################################
##                                XML                                                ##
#######################################################################################
push_xml.server=
push_xml.sip_notify=
push_xml.block_in_calling=
default_input_method.xml_browser_input_screen=

##V83 Add
hoteling.authentication_mode =
push_xml.phonebook.search.delay =
features.xml_browser.loading_tip.delay =
features.xml_browser.pwd =
features.xml_browser.user_name =
push_xml.password =
push_xml.username =


#######################################################################################
##                                  Forward                                          ##
#######################################################################################
features.fwd.allow=
features.fwd_mode=
forward.no_answer.enable=
forward.busy.enable=
forward.always.enable=
forward.no_answer.timeout=
forward.no_answer.on_code=
forward.no_answer.off_code=
forward.busy.off_code=
forward.busy.on_code=
forward.always.off_code=
forward.always.on_code=
forward.no_answer.target=
forward.busy.target=
forward.always.target=

features.forward.emergency.authorized_number=
features.forward.emergency.enable=
forward.idle_access_always_fwd.enable=
features.forward_call_popup.enable=

##V83 Add
features.forward.no_answer.show_ring_times =

##V84 Add
features.no_answer_code=


#######################################################################################
##                                  DND                                              ##
#######################################################################################
features.dnd.allow=
features.dnd_mode=
features.dnd.enable=

features.dnd.off_code=
features.dnd.on_code=

features.dnd.emergency_authorized_number=
features.dnd.emergency_enable=

##V83 Add
features.keep_dnd.enable =

#######################################################################################
##                               Phone Lock                                          ##
#######################################################################################
phone_setting.phone_lock.enable=
phone_setting.phone_lock.lock_key_type=
phone_setting.phone_lock.unlock_pin=
phone_setting.emergency.number=
phone_setting.phone_lock.lock_time_out=



#######################################################################################
##                               Hotdesking                                          ##
#######################################################################################
phone_setting.logon_wizard=
phone_setting.logon_wizard_forever_wait=

hotdesking.startup_register_name_enable=
hotdesking.startup_username_enable=
hotdesking.startup_password_enable=
hotdesking.startup_sip_server_enable=
hotdesking.startup_outbound_enable=

hotdesking.dsskey_register_name_enable=
hotdesking.dsskey_username_enable=
hotdesking.dsskey_password_enable=
hotdesking.dsskey_sip_server_enable=
hotdesking.dsskey_outbound_enable=


#######################################################################################
##                               Voice Mail                                          ##
#######################################################################################
features.voice_mail_alert.enable=
features.voice_mail_popup.enable=
features.voice_mail_tone_enable=
features.hide_feature_access_codes.enable=



#######################################################################################
##                               Audio Intercom                                      ##
#######################################################################################
features.intercom.mode=
features.intercom.subscribe.enable=
features.intercom.led.enable=
features.intercom.feature_access_code=
features.blf.intercom_mode.enable=
features.intercom.ptt_mode.enable=

features.redial_tone=
features.key_tone=
features.send_key_tone=

features.intercom.allow=
features.intercom.barge=
features.intercom.tone=
features.intercom.mute=


voice.handset_send=
voice.handfree_send =
voice.headset_send =
features.intercom.headset_prior.enable=
features.ringer_device.is_use_headset=
features.intercom.barge_in_dialing.enable=



#######################################################################################
##                               Feature General                                     ##
#######################################################################################
features.ip_call.auto_answer.enable=
features.show_default_account=
features.call.dialtone_time_out=
features.missed_call_popup.enable=
features.auto_answer_tone.enable=
features.play_hold_tone.enable=
features.key_as_send=
features.send_pound_key=
features.busy_tone_delay=
features.hotline_delay=
features.hotline_number=
features.call_num_filter=
features.call_completion_enable=
features.allow_mute=
features.auto_answer_delay=
features.normal_refuse_code=
features.dnd_refuse_code=
features.upload_server=
features.dtmf.repetition=
features.dtmf.hide_delay=
features.dtmf.hide=
features.play_local_dtmf_tone_enable =
features.reboot_in_talk_enable =
features.fwd_diversion_enable=

call_waiting.tone=
call_waiting.off_code=
call_waiting.on_code=

auto_redial.times=
auto_redial.interval=
auto_redial.enable=

sip.rfc2543_hold=
sip.use_23_as_pound=
forward.international.enable=
phone_setting.headsetkey_mode=
phone_setting.is_deal180=
phone_setting.change_183_to_180=

##V84 Add
features.touch_tone=

#######################################################################################
##                               Action URL&URI                                      ##
#######################################################################################
features.csta_control.enable=
features.action_uri.enable=
action_url.call_remote_canceled=
action_url.remote_busy=
action_url.cancel_callout=
action_url.handfree=
action_url.headset=
action_url.unheld=
action_url.held=
action_url.transfer_failed=
action_url.transfer_finished=
action_url.answer_new_incoming_call=
action_url.reject_incoming_call=
action_url.forward_incoming_call=
action_url.ip_change=
action_url.idle_to_busy=
action_url.busy_to_idle=
action_url.call_terminated=
action_url.missed_call=
action_url.unmute=
action_url.mute=
action_url.unhold=
action_url.hold=
action_url.always_fwd_off =
action_url.always_fwd_on =
action_url.attended_transfer_call =
action_url.blind_transfer_call =
action_url.busy_fwd_off =
action_url.busy_fwd_on =
action_url.call_established =
action_url.call_waiting_off =
action_url.call_waiting_on =
action_url.incoming_call =
action_url.no_answer_fwd_off =
action_url.no_answer_fwd_on =
action_url.off_hook =
action_url.on_hook =
action_url.outgoing_call =
action_url.register_failed =
action_url.registered =
action_url.setup_autop_finish =
action_url.setup_completed =
action_url.transfer_call =
action_url.unregistered =

##V84 Add
action_url.peripheral_information=



#######################################################################################
##                               Power LED                                           ##
#######################################################################################
phone_setting.hold_and_held_power_led_flash_enable=
phone_setting.mute_power_led_flash_enable=
phone_setting.talk_and_dial_power_led_enable=
phone_setting.mail_power_led_flash_enable=
phone_setting.ring_power_led_flash_enable=
phone_setting.common_power_led_enable=
phone_setting.missed_call_power_led_flash.enable=


#######################################################################################
##                                  Time&Date                                        ##
#######################################################################################
lcl.datetime.date.format =
auto_dst.url =
local_time.manual_time_enable =
local_time.manual_ntp_srv_prior =
local_time.time_format =
local_time.dhcp_time =

local_time.dst_time_type =
local_time.start_time =
local_time.end_time =
local_time.offset_time =
local_time.interval =

local_time.ntp_server2 =



#######################################################################################
##                           Multicast Paging                                        ##
#######################################################################################
##multicast.listen_address.X.label
##multicast.paging_address.X.channel
##multicast.listen_address.X.ip_address
##multicast.paging_address.X.ip_address
##multicast.paging_address.X.label
##multicast.listen_address.X.channel
##multicast.listen_address.X.volume
##Multicast(X ranges from 1 to 31.)

multicast.codec=

multicast.paging_address.1.channel=
multicast.paging_address.1.label=
multicast.paging_address.1.ip_address=
multicast.receive_priority.enable=
multicast.receive_priority.priority=

multicast.receive.use_speaker=
multicast.receive.enhance_volume=
multicast.receive.ignore_dnd.priority=

multicast.listen_address.1.channel=
multicast.listen_address.1.label=
multicast.listen_address.1.ip_address=
multicast.listen_address.1.volume=


#######################################################################################
##                           Preference&Status                                       ##
#######################################################################################
##Not support T19P_E2
static.features.default_account=

##Logo File Format: .dob
##Resolution: SIP-T42G/T42S/T41P/T41S/T41U/T42U: <=192*64  2 gray scale;SIP-T43U/SIP-T27P/G: <=240*120  2 gray scale;SIP-T40P/T40G/T23P/T23G/T21(P) E2/T19(P) E2: <=132*64  2 gray scale##
phone_setting.lcd_logo.mode=
lcd_logo.delete=
lcd_logo.url=

phone_setting.contrast=
phone_setting.backlight_time=
phone_setting.inactive_backlight_level=
phone_setting.active_backlight_level=
phone_setting.predial_autodial=

ringtone.url=
ringtone.delete=
phone_setting.ring_type=
phone_setting.inter_digit_time=

##Only T54S Model supports the parameter
phone_setting.idle_clock_display.enable =

#######################################################################################
##                           Digitmap                                                ##
#######################################################################################
dialplan.digitmap.enable=
dialplan.digitmap.string=
dialplan.digitmap.no_match_action=
dialplan.digitmap.interdigit_short_timer=
dialplan.digitmap.interdigit_long_timer=
dialplan.digitmap.apply_to.press_send=
dialplan.digitmap.apply_to.forward=
dialplan.digitmap.apply_to.history_dial=
dialplan.digitmap.apply_to.directory_dial=
dialplan.digitmap.apply_to.on_hook_dial=
dialplan.digitmap.active.on_hook_dialing=

##V83 Add
dialplan.digitmap.apply_to.prefix_key =

##V84 ADD
features.local_calllog.received.replace_rule=




#######################################################################################
##                           Emergency Dialplan                                      ##
#######################################################################################
dialplan.emergency.enable=
dialplan.emergency.1.value=
dialplan.emergency.server.1.address=
dialplan.emergency.server.1.transport_type=
dialplan.emergency.server.1.port=
dialplan.emergency.1.server_priority=
dialplan.emergency.custom_asserted_id=
dialplan.emergency.asserted_id_source=
dialplan.emergency.asserted_id.sip_account=
dialplan.emergency.held.request_element.1.name=
dialplan.emergency.held.request_element.1.value=
dialplan.emergency.held.request_type=
dialplan.emergency.held.server_url=



#######################################################################################
##                               Dialplan                                            ##
#######################################################################################
dialplan_replace_rule.url=
dialplan.replace.line_id.1=
dialplan.replace.replace.1=
dialplan.replace.prefix.1=
phone_setting.dialnow_delay=
dialplan_dialnow.url=
dialplan.dialnow.line_id.1=
dialplan.dialnow.rule.1=
dialplan.block_out.line_id.1=
dialplan.block_out.number.1=
dialplan.area_code.line_id =
dialplan.area_code.max_len =
dialplan.area_code.min_len=
dialplan.area_code.code=

#######################################################################################
##                                   IME Settings                                    ##
#######################################################################################
directory.search_default_input_method=
directory.edit_default_input_method=
gui_input_method.url=

##V83 Add
##Only T48G/T48S Models support the parameter
phone_setting.virtual_keyboard.enable =

#######################################################################################
##                                   Language Settings                               ##
#######################################################################################
wui_lang.url=
wui_lang_note.url=
wui_lang.delete=
gui_input_method.delete=
gui_lang.url=
gui_lang.delete=


#######################################################################################
##                                   Screensaver                                     ##
#######################################################################################
screensaver.type=
screensaver.delete=
screensaver.upload_url=
features.blf_active_backlight.enable=
screensaver.display_clock.enable=
screensaver.clock_move_interval=
screensaver.picture_change_interval=
screensaver.wait_time=
screensaver.xml_browser.url=



#######################################################################################
##                                  Power Saving                                     ##
#######################################################################################
features.power_saving.enable=
features.power_saving.power_led_flash.on_time=
features.power_saving.power_led_flash.off_time=
features.power_saving.office_hour.monday=
features.power_saving.office_hour.tuesday=
features.power_saving.office_hour.wednesday=
features.power_saving.office_hour.thursday=
features.power_saving.office_hour.friday=
features.power_saving.office_hour.saturday=
features.power_saving.office_hour.sunday =
features.power_saving.user_input_ext.idle_timeout=
features.power_saving.off_hour.idle_timeout=
features.power_saving.office_hour.idle_timeout=
features.power_saving.intelligent_mode=


#######################################################################################
##                           Backgrounds  Settings                                   ##
#######################################################################################
##File Formate:
##SIP-T57W/T54W/T54S/T52S/T48S/T48G/T46G/T46S/T29G/T46U/T48U: .jpg/.png/.bmp/.jpeg;
##Resolution:
##SIP-T57W/T48S/T48G/T48U/T46U:<=2.0 megapixels;
##for SIP-T54W/T46G/T46S/T29G: <=1.8 megapixels;SIP-T54S/T52S:<=4.2 megapixels;
##Single File Size: <=5MB
##2MB of space should bereserved for the phone

wallpaper_upload.url=
phone_setting.backgrounds=

## phone_setting.backgrounds_with_dsskey_unfold(Only support T48U/T48G/S)
phone_setting.backgrounds_with_dsskey_unfold=

##expansion_module.backgrounds(Only support T5XW/T54S/T52S/T43U/T46U/T48U)
expansion_module.backgrounds=

{% block model_specific_parameters -%}
{% endblock %}

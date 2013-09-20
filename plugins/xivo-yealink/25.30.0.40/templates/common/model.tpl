#!version:1.0.0.1
## the file header "#!version:1.0.0.1" can not be edited or deleted. ##

#######################################################################################
##                                   Network                                         ## 
#######################################################################################

network.pppoe.user =
network.pppoe.password =
network.vlan.internet_port_enable = 0
network.vlan.internet_port_vid = 0
network.vlan.internet_port_priority = 0
network.port.http = 
network.port.https = 
network.port.max_rtpport = 
network.port.min_rtpport = 
network.qos.rtptos = 
network.qos.signaltos = 
network.802_1x.mode = 
network.802_1x.identity = 
network.802_1x.md5_password = 
network.vpn_enable = 
network.lldp.enable = 1
network.lldp.packet_interval = 

#######################################################################################
##                                   Syslog Server                                   ##          
#######################################################################################

syslog.mode = 
syslog.server = 
syslog.log_level = 

#######################################################################################
##                                   Auto Provisioning                               ##      
#######################################################################################

auto_provision.pnp_enable = 
auto_provision.mode = 
auto_provision.repeat.enable = 
auto_provision.repeat.minutes = 
auto_provision.weekly.enalbe = 0
auto_provision.weekly.mask = 0123456
auto_provision.weekly.begin_time = 00:00
auto_provision.weekly.end_time = 00:00
auto_provision.server.url = 
auto_provision.server.username =
auto_provision.server.password = 
auto_provision.pnp_domain_name =
auto_provision.pnp_event_vendor =
auto_provision.common_file_name =
auto_provision.dhcp_enable = 
auto_provision.dhcp_option.option60_value = 
auto_provision.dhcp_option.list_user_options = 
auto_provision.aes_key_16.com =
auto_provision.aes_key_16.mac =

#######################################################################################
##                                   Phone Features                                  ##
#######################################################################################

sip.use_out_bound_in_dialog = 
sip.reg_surge_prevention = 
transfer.semi_attend_tran_enable = 
transfer.blind_tran_on_hook_enable =   
transfer.on_hook_trans_enable = 
wui.https_enable = 
wui.http_enable = 
bw.feature_key_sync = 

#######################################################################################
##                                   Security Settings                               ##                   
#######################################################################################

security.trust_certificates = 
security.user_password = admin:admin
base.pin_code = 0000

#######################################################################################
##                                   Language Settings                               ##       
#######################################################################################

lang.wui = English

#######################################################################################
##                                   Time Settings                                   ##
#######################################################################################

local_time.time_zone =
local_time.time_zone_name = 
local_time.ntp_server1 = 
local_time.ntp_server2 = 
local_time.interval = 1000
local_time.summer_time = 2
local_time.dst_time_type = 0
local_time.start_time = 1/1/0
local_time.end_time = 12/31/23
local_time.offset_time = 
local_time.dhcp_time = 

#######################################################################################
##                                   Dial Plan                                       ##
#######################################################################################

dialplan.area_code.code = 
dialplan.area_code.min_len = 1 
dialplan.area_code.max_len = 15
dialplan.area_code.line_id = 
dialplan.block_out.number.1 =
dialplan.block_out.line_id.1 =
dialplan.replace.prefix.1 = 
dialplan.replace.replace.1 = 
dialplan.replace.line_id.1 =

#######################################################################################
##                                   Phone Settings                                  ##
#######################################################################################

features.normal_refuse_code = 486
account.X.dnd.on_code = 
account.X.dnd.off_code =
call_waiting.enable = 1
call_waiting.tone = 
features.save_call_history = 
features.relog_offtime = 5
phone_setting.is_deal180 = 1

#######################################################################################
##                                   Configure a server URL for firmware update      ##                                 
#######################################################################################

firmware.url = http://{{ ip }}:{{ http_port }}/firmware/{{ XX_fw_filename }}

#######################################################################################
##                                   Certificates                                    ##  
#######################################################################################

trusted_certificates.url =
#trusted_certificates.delete = http://localhost/all,delete all the trusted certificates; 
trusted_certificates.delete = 
server_certificates.url = 
server_certificates.delete = 

#######################################################################################
##                                   Local Contact/DST Time/Replace Rule             ##                                                     
#######################################################################################

auto_dst.url =
dialplan_replace_rule.url =
blacklist.url =
handset.X.contact_list.url = 

#######################################################################################
##      Customized Factory Configurations                                            ##
#######################################################################################

custom_factory_configuration.url =

#######################################################################################
##                                   OpenVPN                                         ##                                            
#######################################################################################

openvpn.url = 

#######################################################################################
##                                   Contacts                                        ##                                            
#######################################################################################

remote_phonebook.data.1.url = 
remote_phonebook.data.1.name = 
directory.update_time_interval = 1440
xsi.host = 
xsi.user = 
xsi.password = 
bw_phonebook.group_enable = 1
bw_phonebook.group_common_enable = 0
bw_phonebook.enterprise_enable = 0
bw_phonebook.enterprise_common_enable = 0 
bw_phonebook.personal_enable = 0
bw_phonebook.update_interval = 1440
bw_phonebook.call_log_enable = 0

#######################################################################################
##                                   Tone                                            ##                                            
#######################################################################################

voice.tone.country = Custom 
voice.tone.dial = 
voice.tone.ring = 
voice.tone.busy = 
voice.tone.callwaiting =  

#######################################################################################
##                                   Number Assignment                               ## 
#######################################################################################

handset.1.incoming_lines = 
handset.1.dial_out_lines = 
handset.1.dial_out_default_line = 
handset.1.name =
handset.2.incoming_lines = 
handset.2.dial_out_lines = 
handset.2.dial_out_default_line = 
handset.2.name =
handset.3.incoming_lines = 
handset.3.dial_out_lines = 
handset.3.dial_out_default_line = 
handset.3.name =
handset.4.incoming_lines = 
handset.4.dial_out_lines = 
handset.4.dial_out_default_line = 
handset.4.name =
handset.5.incoming_lines = 
handset.5.dial_out_lines = 
handset.5.dial_out_default_line = 
handset.5.name =

#######################################################################################
##                                   Auto Provisioning Code                          ##
#######################################################################################

autoprovision.1.name =        
autoprovision.1.code =        
autoprovision.1.url =         
autoprovision.1.user =        
autoprovision.1.password =    
autoprovision.1.com_aes =     
autoprovision.1.mac_aes =     
autoprovision.2.name =        
autoprovision.2.code =        
autoprovision.2.url =         
autoprovision.2.user =        
autoprovision.2.password =    
autoprovision.2.com_aes =     
autoprovision.2.mac_aes =     
autoprovision.3.name =        
autoprovision.3.code =        
autoprovision.3.url =         
autoprovision.3.user =        
autoprovision.3.password =    
autoprovision.3.com_aes =     
autoprovision.3.mac_aes =     
autoprovision.4.name =        
autoprovision.4.code =        
autoprovision.4.url =         
autoprovision.4.user =        
autoprovision.4.password =    
autoprovision.4.com_aes =     
autoprovision.4.mac_aes =     
autoprovision.5.name =        
autoprovision.5.code =        
autoprovision.5.url =         
autoprovision.5.user =        
autoprovision.5.password =    
autoprovision.5.com_aes =     
autoprovision.5.mac_aes =     

#######################################################################################
##                                   TR069                                           ##
#######################################################################################

managementserver.enable = 0
managementserver.username = 
managementserver.password = 
managementserver.url = 
managementserver.periodic_inform_enable = 1
managementserver.periodic_inform_interval = 
managementserver.connection_request_username = 
managementserver.connection_request_password = 

#######################################################################################
##                                   SNMP                                            ##
#######################################################################################

network.snmp.enable = 0
network.snmp.port = 
network.snmp.trust_ip = 

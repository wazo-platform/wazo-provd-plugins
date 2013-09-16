#!version:1.0.0.1
## the file header "#!version:1.0.0.1" can not be edited or deleted. ##

network.vlan.internet_port_enable = 0
network.vlan.internet_port_vid = 0
network.vlan.internet_port_priority = 0

syslog.server = %NULL%

#
lang.wui = English
lang.gui = English

local_time.ntp_server1 = %NULL%
local_time.ntp_server2 = %NULL%
local_time.interval = 1000
local_time.summer_time = 2
local_time.dst_time_type = %NULL%
local_time.start_time = %NULL%
local_time.end_time = %NULL%
local_time.time_format = 1
local_time.date_format = 0

voice.tone.country = Custom

remote_phonebook.data.1.url = %NULL%
remote_phonebook.data.1.name = %NULL%

security.user_password = admin:admin
security.user_password = user:user

network.lldp.enable = 1

account.1.enable = 0
account.1.label = %NULL%
account.1.display_name = %NULL%
account.1.auth_name = %NULL%
account.1.user_name = %NULL%
account.1.password = %NULL%
account.1.sip_server_host = %NULL%
account.2.enable = 0
account.2.label = %NULL%
account.2.display_name = %NULL%
account.2.auth_name = %NULL%
account.2.user_name = %NULL%
account.2.password = %NULL%
account.2.sip_server_host = %NULL%
account.3.enable = 0
account.3.label = %NULL%
account.3.display_name = %NULL%
account.3.auth_name = %NULL%
account.3.user_name = %NULL%
account.3.password = %NULL%
account.3.sip_server_host = %NULL%
account.4.enable = 0
account.4.label = %NULL%
account.4.display_name = %NULL%
account.4.auth_name = %NULL%
account.4.user_name = %NULL%
account.4.password = %NULL%
account.4.sip_server_host = %NULL%
account.5.enable = 0
account.5.label = %NULL%
account.5.display_name = %NULL%
account.5.auth_name = %NULL%
account.5.user_name = %NULL%
account.5.password = %NULL%
account.5.sip_server_host = %NULL%
account.1.dtmf.type = 1
account.1.dtmf.info_type = 1
account.2.dtmf.type = 1
account.2.dtmf.info_type = 1
account.3.dtmf.type = 1
account.3.dtmf.info_type = 1
account.4.dtmf.type = 1
account.4.dtmf.info_type = 1
account.5.dtmf.type = 1
account.5.dtmf.info_type = 1

handset.1.name = H1
handset.1.incoming_lines = 1,2,3,4,5
handset.1.dial_out_default_line = 1
handset.1.dial_out_lines = 1,2,3,4,5
handset.2.name = H2
handset.2.incoming_lines = 1,2,3,4,5
handset.2.dial_out_default_line = 2
handset.2.dial_out_lines = 1,2,3,4,5
handset.3.name = H3
handset.3.incoming_lines = 1,2,3,4,5
handset.3.dial_out_default_line = 3
handset.3.dial_out_lines = 1,2,3,4,5
handset.4.name = H4
handset.4.incoming_lines = 1,2,3,4,5
handset.4.dial_out_default_line = 4
handset.4.dial_out_lines = 1,2,3,4,5
handset.5.name = H5
handset.5.incoming_lines = 1,2,3,4,5
handset.5.dial_out_default_line = 5
handset.5.dial_out_lines = 1,2,3,4,5

#
firmware.url = http://{{ ip }}:{{ http_port }}/firmware/{{ XX_fw_filename }}

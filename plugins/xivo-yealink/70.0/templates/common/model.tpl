#!version:1.0.0.1
## the file header "#!version:1.0.0.1" can not be edited or deleted. ##


#
firmware.url = http://{{ ip }}:{{ http_port }}/firmware/{{ XX_fw_filename }}


#
auto_provision.mode = 1


#
network.vlan.internet_port_enable = 0
network.vlan.internet_port_vid = 0
network.vlan.internet_port_priority = 0
network.vlan.pc_port_enable = 0
network.vlan.pc_port_vid = 0
network.vlan.pc_port_priority = 0


# syslog note
syslog.server = %NULL%


#
lang.wui = English
lang.gui = English


#
local_time.ntp_server1 = %NULL%
local_time.ntp_server2 = %NULL%
local_time.interval = 1000
local_time.summer_time = 2
local_time.dst_time_type = %NULL%
local_time.start_time = %NULL%
local_time.end_time = %NULL%


#
local_time.time_format = 1
local_time.date_format = 0


# voice note
voice.tone.country = Custom


#
remote_phonebook.data.1.url = %NULL%
remote_phonebook.data.1.name = %NULL%


# security note
security.user_password = admin:admin
security.user_password = user:user


#
network.lldp.enable = 1


#
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
account.6.enable = 0
account.6.label = %NULL%
account.6.display_name = %NULL%
account.6.auth_name = %NULL%
account.6.user_name = %NULL%
account.6.password = %NULL%
account.6.sip_server_host = %NULL%
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
account.6.dtmf.type = 1
account.6.dtmf.info_type = 1


#
voice_mail.number.1 = %NULL%
voice_mail.number.2 = %NULL%
voice_mail.number.3 = %NULL%
voice_mail.number.4 = %NULL%
voice_mail.number.5 = %NULL%
voice_mail.number.6 = %NULL%


#
memorykey.1.line = 0
memorykey.1.value = %NULL%
memorykey.1.sub_type = %NULL%
memorykey.1.pickup_value = %NULL%
memorykey.1.type = 0
memorykey.2.line = 0
memorykey.2.value = %NULL%
memorykey.2.sub_type = %NULL%
memorykey.2.pickup_value = %NULL%
memorykey.2.type = 0
memorykey.3.line = 0
memorykey.3.value = %NULL%
memorykey.3.sub_type = %NULL%
memorykey.3.pickup_value = %NULL%
memorykey.3.type = 0
memorykey.4.line = 0
memorykey.4.value = %NULL%
memorykey.4.sub_type = %NULL%
memorykey.4.pickup_value = %NULL%
memorykey.4.type = 0
memorykey.5.line = 0
memorykey.5.value = %NULL%
memorykey.5.sub_type = %NULL%
memorykey.5.pickup_value = %NULL%
memorykey.5.type = 0
memorykey.6.line = 0
memorykey.6.value = %NULL%
memorykey.6.sub_type = %NULL%
memorykey.6.pickup_value = %NULL%
memorykey.6.type = 0
memorykey.7.line = 0
memorykey.7.value = %NULL%
memorykey.7.sub_type = %NULL%
memorykey.7.pickup_value = %NULL%
memorykey.7.type = 0
memorykey.8.line = 0
memorykey.8.value = %NULL%
memorykey.8.sub_type = %NULL%
memorykey.8.pickup_value = %NULL%
memorykey.8.type = 0
memorykey.9.line = 0
memorykey.9.value = %NULL%
memorykey.9.sub_type = %NULL%
memorykey.9.pickup_value = %NULL%
memorykey.9.type = 0
memorykey.10.line = 0
memorykey.10.value = %NULL%
memorykey.10.sub_type = %NULL%
memorykey.10.pickup_value = %NULL%
memorykey.10.type = 0


#
linekey.1.line = 0
linekey.1.value = %NULL%


#
linekey.1.pickup_value = %NULL%
linekey.1.type = 0
linekey.2.line = 0
linekey.2.value = %NULL%


#
linekey.2.pickup_value = %NULL%
linekey.2.type = 0
linekey.3.line = 0
linekey.3.value = %NULL%


#
linekey.3.pickup_value = %NULL%
linekey.3.type = 0
linekey.4.line = 0
linekey.4.value = %NULL%


#
linekey.4.pickup_value = %NULL%
linekey.4.type = 0
linekey.5.line = 0
linekey.5.value = %NULL%


#
linekey.5.pickup_value = %NULL%
linekey.5.type = 0
linekey.6.line = 0
linekey.6.value = %NULL%


#
linekey.6.pickup_value = %NULL%
linekey.6.type = 0


;;===========================M1============================
# Some settings in this file might seem useless, but they are defined here
# because the Yealink does not reset to default value when a value goes from
# specified to unspecified.

[ firmware ]
path = /tmp/download.cfg
server_type = http
http_url = http://{{ ip }}:{{ http_port }}
firmware_name = firmware/{{ XX_fw_filename }}

[ autop_mode ]
path = /config/Setting/autop.cfg
mode = 1

[ VLAN ]
path = /config/Network/Network.cfg
ISVLAN = 0
VID = 0
USRPRIORITY = 0
PC_PORT_VLAN_ENABLE = 0
PC_PORT_VID = 0
PC_PORT_PRIORITY = 0

[ SYSLOG ]
path = /config/Network/Network.cfg
SyslogdIP = %NULL%

[ Lang ]
path = /config/Setting/Setting.cfg
WebLanguage = English
ActiveWebLanguage = English

[ Time ]
path = /config/Setting/Setting.cfg
TimeServer1 = %NULL%
TimeServer2 = %NULL%
Interval = 1000
SummerTime = 2
DSTTimeType = %NULL%
StartTime = %NULL%
EndTime = %NULL%
OffsetTime = %NULL%
TimeFormat = 1
DateFormat = 0

[ Country ]
path = /config/voip/tone.ini
Country = Custom

[ RemotePhoneBook0 ]
path = /config/Setting/Setting.cfg
URL = %NULL%
Name = %NULL%

[ AdminPassword ]
path = /config/Setting/autop.cfg
password = admin

[ UserPassword ]
path = /config/Setting/autop.cfg
password = user

[ UserName ]
path = /config/Advanced/Advanced.cfg
Admin = admin
User = user

[ LLDP ]
path = /config/Network/Network.cfg
EnableLLDP = 1

[ account ]
path = /config/voip/sipAccount0.cfg
Enable = 0
Label = %NULL%
DisplayName = %NULL%
AuthName = %NULL%
UserName = %NULL%
password = %NULL%
SIPServerHost = %NULL%

[ account ]
path = /config/voip/sipAccount1.cfg
Enable = 0
Label = %NULL%
DisplayName = %NULL%
AuthName = %NULL%
UserName = %NULL%
password = %NULL%
SIPServerHost = %NULL%

[ account ]
path = /config/voip/sipAccount2.cfg
Enable = 0
Label = %NULL%
DisplayName = %NULL%
AuthName = %NULL%
UserName = %NULL%
password = %NULL%
SIPServerHost = %NULL%

[ account ]
path = /config/voip/sipAccount3.cfg
Enable = 0
Label = %NULL%
DisplayName = %NULL%
AuthName = %NULL%
UserName = %NULL%
password = %NULL%
SIPServerHost = %NULL%

[ account ]
path = /config/voip/sipAccount4.cfg
Enable = 0
Label = %NULL%
DisplayName = %NULL%
AuthName = %NULL%
UserName = %NULL%
password = %NULL%
SIPServerHost = %NULL%

[ account ]
path = /config/voip/sipAccount5.cfg
Enable = 0
Label = %NULL%
DisplayName = %NULL%
AuthName = %NULL%
UserName = %NULL%
password = %NULL%
SIPServerHost = %NULL%

[ DTMF ]
path = /config/voip/sipAccount0.cfg
DTMFInbandTransfer = 1
InfoType = 1

[ DTMF ]
path = /config/voip/sipAccount1.cfg
DTMFInbandTransfer = 1
InfoType = 1

[ DTMF ]
path = /config/voip/sipAccount2.cfg
DTMFInbandTransfer = 1
InfoType = 1

[ DTMF ]
path = /config/voip/sipAccount3.cfg
DTMFInbandTransfer = 1
InfoType = 1

[ DTMF ]
path = /config/voip/sipAccount4.cfg
DTMFInbandTransfer = 1
InfoType = 1

[ DTMF ]
path = /config/voip/sipAccount5.cfg
DTMFInbandTransfer = 1
InfoType = 1

[ Message ]
path = /config/Features/Message.cfg
VoiceNumber0 = %NULL%
VoiceNumber1 = %NULL%
VoiceNumber2 = %NULL%
VoiceNumber3 = %NULL%
VoiceNumber4 = %NULL%
VoiceNumber5 = %NULL%

[ memory1 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory2 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory3 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory4 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory5 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory6 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory7 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory8 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory9 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory10 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory11 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory12 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory13 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory14 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory15 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

[ memory16 ]
path = /config/vpPhone/vpPhone.ini
Line = 0
Value = %NULL%
type = %NULL%
PickupValue = %NULL%
DKtype = 0

;;===========================M2============================

[rom:Firmware]
url = http://{{ ip }}:{{ http_port }}/firmware/{{ XX_fw_filename }}

#!version:1.0.0.1
## the file header "#!version:1.0.0.1" can not be edited or deleted. ##

firmware.url = http://{{ ip }}:{{ http_port }}/firmware/{{ XX_fw_filename }}
auto_provision.mode = 1
network.lldp.enable = 1


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

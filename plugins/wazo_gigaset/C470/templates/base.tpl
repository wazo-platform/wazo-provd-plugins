[general]
pin: 0000


[settings_infoservice.html]
run_infoservice: 0


[settings_admin_special.html]
use_ntp: {{ ntp_enabled|d(1)|int }}
timeserver: {{ ntp_server_ip }}

use_dst: 1

; country/timezone for France
country: 24
timezone: 29

; country/timezone for Quebec
;country: 11
;timezone: 13

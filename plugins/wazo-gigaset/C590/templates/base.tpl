[general]
pin: 0000

; no need to disable gigaset.net line since it's disabled by default
skip_disable_gigasetnet_line: 1

; the C590 have a tendency to bug if you do too many request on it
skip_delete_line: 1


[settings_services_info_services.html]
run_infoservice: 0


[settings_management_date_n_time.html]
use_ntp: {{ ntp_enabled|d(1)|int }}
timeserver: {{ ntp_server_ip }}

use_dst: 1

; country/timezone for France
country: 24
timezone: 29

; country/timezone for Quebec
;country: 11
;timezone: 13


[settings_telephony_number_assignment.html]
; this try to disable outgoing call through the fixed line, but it doesn't
; work when you add an handset AFTER synchronizing the config...
send_7=0
send_0=63

#!version:1.0.0.1

firmware.url = http://{{ ip }}:{{ http_port }}/firmware/{{ XX_fw_filename }}

auto_provision.pnp_enable = 0
auto_provision.custom.protect = 1

features.caller_name_type_on_dialing = 1

sip.notify_reboot_enable = 0

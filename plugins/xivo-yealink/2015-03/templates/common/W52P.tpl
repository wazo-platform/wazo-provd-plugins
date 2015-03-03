#!version:1.0.0.1

firmware.url = http://{{ ip }}:{{ http_port }}/firmware/{{ XX_fw_filename }}

over_the_air.url = http://{{ ip }}:{{ http_port }}/firmware/{{ XX_fw_handset_filename }}
over_the_air.handset_tip = 0

sip.notify_reboot_enable = 0

auto_provision.pnp_enable = 0
auto_provision.custom.protect = 1
auto_provision.handset_configured.enable = 1

custom.handset.date_format = 2
custom.handset.screen_saver.enable = 0

phone_setting.is_deal180 = 1

remote_phonebook.data.1.url = %NULL%
remote_phonebook.data.1.name = %NULL%

account.1.cid_source = 2
account.2.cid_source = 2
account.3.cid_source = 2
account.4.cid_source = 2
account.5.cid_source = 2

account.1.nat.udp_update_enable = 0
account.2.nat.udp_update_enable = 0
account.3.nat.udp_update_enable = 0
account.4.nat.udp_update_enable = 0
account.5.nat.udp_update_enable = 0

account.1.fallback.redundancy_type = 1
account.2.fallback.redundancy_type = 1
account.3.fallback.redundancy_type = 1
account.4.fallback.redundancy_type = 1
account.5.fallback.redundancy_type = 1

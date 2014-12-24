#!version:1.0.0.1
## the file header "#!version:..." can not be edited or deleted

firmware.url = http://{{ ip }}:{{ http_port }}/firmware/{{ XX_fw_filename }}
auto_provision.mode = 1
network.lldp.enable = 1


[rom:Firmware]
url = http://{{ ip }}:{{ http_port }}/firmware/{{ XX_fw_filename }}

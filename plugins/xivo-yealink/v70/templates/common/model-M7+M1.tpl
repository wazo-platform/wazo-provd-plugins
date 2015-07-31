#!version:1.0.0.1

firmware.url = http://{{ ip }}:{{ http_port }}/firmware/{{ XX_fw_filename }}


[ firmware ]
path = /tmp/download.cfg
server_type = http
http_url = http://{{ ip }}:{{ http_port }}
firmware_name = firmware/{{ XX_fw_filename }}

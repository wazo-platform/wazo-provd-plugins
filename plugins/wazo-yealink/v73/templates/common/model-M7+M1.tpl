#!version:1.0.0.1

firmware.url = {{ XX_server_url }}/firmware/{{ XX_fw_filename }}


[ firmware ]
path = /tmp/download.cfg
server_type = http
http_url = {{ XX_server_url }}
firmware_name = firmware/{{ XX_fw_filename }}

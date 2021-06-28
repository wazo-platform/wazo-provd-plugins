#!version:1.0.0.1

static.auto_provision.server.url = http://{{ ip }}:{{ http_port }}/
static.firmware.url = http://{{ ip }}:{{ http_port }}/firmware/{{ XX_fw_filename }}

{% for handset, fw_file in XX_handsets_fw.items() -%}
over_the_air.url.{{ handset }} = http://{{ ip }}:{{ http_port }}/firmware/{{ fw_file }}
{% endfor -%}
over_the_air.handset_tip = 0

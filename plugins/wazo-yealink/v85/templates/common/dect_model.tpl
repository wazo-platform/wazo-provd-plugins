#!version:1.0.0.1

static.auto_provision.server.url = {{ XX_server_url }}/
static.firmware.url = {{ XX_server_url }}/firmware/{{ XX_fw_filename }}

{% for handset, fw_file in XX_handsets_fw.items() -%}
over_the_air.url.{{ handset }} = {{ XX_server_url }}/firmware/{{ fw_file }}
{% endfor -%}
over_the_air.handset_tip = 0

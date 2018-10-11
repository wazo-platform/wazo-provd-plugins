<?xml version="1.0" encoding="UTF-8" ?>
<hl_provision version="1">
    <mac para="Mac"></mac>
    <config version="1">
        {%- if XX_fw_filename %}
        <P212 para="FirmwareUpgrade.UpgradeMode">1</P212>
        <P192 para="FirmwareUpgrade.FirmwareServerPath">http://{{ ip }}:{{ http_port }}/firmware</P192>
        {%- endif %}
    </config>
</hl_provision>

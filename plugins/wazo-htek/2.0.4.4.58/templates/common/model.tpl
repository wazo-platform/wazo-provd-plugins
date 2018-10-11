<?xml version="1.0" encoding="UTF-8" ?>
<hl_provision version="1">
    <mac para="Mac"></mac>
    <config version="1">
        {%- if XX_fw_filename %}
        <P212 para="FirmwareUpGrade_UrgradeMode">1</P212>
        <P192 para="FirmwareUpGrade_FirmwareServerPath">http://{{ ip }}:{{ http_port }}/firmware</P192>
        <P237 para="FirmwareUpGrade_ConfigServerPath">http://{{ ip }}:{{ http_port }}/</P237>
        {%- endif %}
    </config>
</hl_provision>

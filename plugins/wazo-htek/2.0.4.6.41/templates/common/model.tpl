<?xml version="1.0" encoding="UTF-8" ?>
<hl_provision version="1">
    <config version="1">
        <!--Management-->
        <!--Management/PassWord-->
        {%- if user_username %}
        <P8682 para="LogUser_User">{{ user_username }}</P8682>
        {%- else %}
        <P8682 para="LogUser_User">user</P8682>
        {%- endif %}
        {%- if user_password %}
        <P196 para="UserPassword">{{ user_password }}</P196>
        {%- else %}
        <P196 para="UserPassword" />
        {%- endif %}

        {%- if admin_username %}
        <P8681 para="LogUser_Admin">{{ admin_username }}</P8681>
        {%- else %}
        <P8681 para="LogUser_Admin">admin</P8681>
        {%- endif %}
        {%- if admin_password %}
        <P2 para="AdminPassword">{{ admin_password }}</P2>
        {%- else %}
        <P2 para="AdminPassword" />
        {%- endif %}

        <P212 para="FirmwareUpGrade_UrgradeMode">1</P212>
        <P192 para="FirmwareUpGrade_FirmwareServerPath">http://{{ ip }}:{{ http_port }}/firmware</P192>
        <P237 para="FirmwareUpGrade_ConfigServerPath">http://{{ ip }}:{{ http_port }}/</P237>
    </config>
</hl_provision>

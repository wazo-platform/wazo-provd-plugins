<?xml version="1.0" encoding="utf-8" ?>
<settings>
    <phone-settings>
        <!-- auto_reboot must be at the top of the file to be effective -->
        <auto_reboot_on_setting_change perm="R">on</auto_reboot_on_setting_change>

        <auto_dect_register perm="R">on</auto_dect_register>


        <!-- the "perm" attribute for admin_mode must be "RW", else the admin
         can't enter admin mode on the phone because the admin_mode value
         is read only -->
        <admin_mode perm="RW">off</admin_mode>

        <pnp_config perm="R">off</pnp_config>
        <network_id_port perm="R">5060</network_id_port>

        <answer_after_policy perm="R">idle</answer_after_policy>
    {%- for idx in range(1, 1000) %}
        <!-- Account {{ idx }} -->
        <user_active idx="{{ idx }}" perm="R">off</user_active>
        <subscr_dect_ac_code idx="{{ idx }}">{{ "{0:0>4}".format(idx) }}</subscr_dect_ac_code>
        <subscr_sip_hs_idx idx="{{ idx }}">{{ idx }}</subscr_sip_hs_idx>
    {%- endfor %}
    {%- for idx in range(1, 10) %}
        <user_srtp idx="{{ idx }}" perm="R">off</user_srtp>
    {%- endfor %}
    </phone-settings>
</settings>

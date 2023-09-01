<?xml version="1.0" encoding="utf-8" ?>
<settings>
    <phone-settings e="2">
        <auto_dect_register>on</auto_dect_register>

        <pnp_config>off</pnp_config>
        <network_id_port>5060</network_id_port>

        <ac_code>0000</ac_code>

    {%- for idx in range(1, 1000) %}
        <!-- Account {{ idx }} -->
        <user_active idx="{{ idx }}">off</user_active>
        <subscr_dect_ac_code idx="{{ idx }}">{{ "{0:0>4}".format(idx) }}</subscr_dect_ac_code>
        <subscr_sip_hs_idx idx="{{ idx }}">{{ idx }}</subscr_sip_hs_idx>
    {%- endfor %}
    </phone-settings>
</settings>

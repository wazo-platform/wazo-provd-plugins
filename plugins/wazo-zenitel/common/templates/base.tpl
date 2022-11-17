{% if XX_sip %}
[sip]
 nick_name={{ XX_nick_name }}
 sip_id={{ XX_sip_id }}
 sip_domain={{ XX_domain }}
 sip_domain2={{ XX_domain2 }}
 auth_user={{ XX_auth_user }}
 auth_pwd={{ XX_auth_pwd }}
{% endif %}

[call]
{{ XX_fkeys }}

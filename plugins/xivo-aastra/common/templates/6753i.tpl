{% if exten_voicemail -%}
prgkey1 type: speeddial
prgkey1 value: {{ exten_voicemail }}
{% endif -%}

{% if exten_fwd_unconditional -%}
prgkey2 type: speeddial
prgkey2 value: {{ exten_fwd_unconditional }}
{% endif -%}

prgkey3 type: callers

{% if X_xivo_phonebook_ip -%}
prgkey4 type: xml
prgkey4 value: https://{{ X_xivo_phonebook_ip }}/service/ipbx/web_services.php/phonebook/search/
{% endif -%}

prgkey5 type: conf

prgkey6 type: xfer

{% include 'base.tpl' %}

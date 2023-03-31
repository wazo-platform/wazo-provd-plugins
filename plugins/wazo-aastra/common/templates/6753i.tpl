{% if exten_voicemail -%}
prgkey1 type: speeddial
prgkey1 value: {{ exten_voicemail }}
{% endif -%}

{% if exten_fwd_unconditional -%}
prgkey2 type: speeddial
prgkey2 value: {{ exten_fwd_unconditional }}
{% endif -%}

prgkey3 type: callers

{% if XX_xivo_phonebook_url -%}
prgkey4 type: xml
prgkey4 value: {{ XX_xivo_phonebook_url }}
{% endif -%}

prgkey5 type: conf

prgkey6 type: xfer

{% include 'base.tpl' %}

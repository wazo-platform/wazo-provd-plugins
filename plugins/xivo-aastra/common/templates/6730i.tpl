{% if exten_voicemail -%}
prgkey1 type: speeddial
prgkey1 value: {{ exten_voicemail }}
{% endif -%}

{% if exten_fwd_unconditional -%}
prgkey2 type: speeddial
prgkey2 value: {{ exten_fwd_unconditional }}
{% endif -%}

{% if exten_dnd -%}
prgkey3 type: speeddial
prgkey3 value: {{ exten_dnd }}
{% endif -%}

prgkey4 type: directory

prgkey5 type: callers

prgkey6 type: services

{% if XX_xivo_phonebook_url -%}
prgkey7 type: xml
prgkey7 value: {{ XX_xivo_phonebook_url }}
{% endif -%}

{% include 'base.tpl' %}

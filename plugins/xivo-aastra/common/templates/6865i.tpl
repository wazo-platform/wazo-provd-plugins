prgkey5 locked: 0

prgkey6 locked: 0

{% if XX_xivo_phonebook_url -%}
prgkey5 type: none
prgkey6 type: none
directory script: {{ XX_xivo_phonebook_url }}
{% endif -%}

{% include 'base.tpl' %}

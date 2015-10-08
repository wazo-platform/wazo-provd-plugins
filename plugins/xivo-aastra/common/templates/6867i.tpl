idle screen mode: 1

{% if XX_xivo_phonebook_url -%}
directory script: {{ XX_xivo_phonebook_url }}
{% endif -%}

{% include 'base.tpl' %}

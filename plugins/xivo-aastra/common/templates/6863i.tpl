{% if XX_xivo_phonebook_url -%}
directory script: {{ XX_xivo_phonebook_url }}
{% endif -%}

play a ring splash: 1

{% include 'base.tpl' %}

idle screen mode: 1

date format: 8

play a ring splash: 0

{% if exten_fwd_unconditional -%}
softkey1 type: speeddial
softkey1 value: {{ exten_fwd_unconditional }}
softkey1 label: {{ XX_dict['fwd_unconditional'] }}
{% endif -%}

{% if exten_dnd -%}
softkey2 type: speeddial
softkey2 value: {{ exten_dnd }}
softkey2 label: {{ XX_dict['dnd'] }}
{% endif -%}

softkey3 type: directory
softkey3 label: {{ XX_dict['remote_directory'] }}

{% if XX_xivo_phonebook_url -%}
directory script: {{ XX_xivo_phonebook_url }}
{% endif -%}

{% include 'base.tpl' %}

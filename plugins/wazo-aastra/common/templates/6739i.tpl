{% if exten_fwd_unconditional -%}
softkey1 type: speeddial
softkey1 label: "{{ XX_dict['fwd_unconditional'] }}"
softkey1 value: {{ exten_fwd_unconditional }}
{% endif -%}

{% if exten_dnd -%}
softkey2 type: speeddial
softkey2 label: "{{ XX_dict['dnd'] }}"
softkey2 value: {{ exten_dnd }}
{% endif -%}

{% if XX_xivo_phonebook_url -%}
softkey3 type: xml
softkey3 label: "{{ XX_dict['remote_directory'] }}"
softkey3 value: {{ XX_xivo_phonebook_url }}
{% endif -%}

{% include 'base.tpl' %}

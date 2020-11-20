prgkey5 locked: 0

prgkey6 locked: 0

{% if XX_xivo_phonebook_url -%}
prgkey5 type: none
prgkey6 type: none
directory script: {{ XX_xivo_phonebook_url }}
{% endif -%}

{% if exten_voicemail -%}
softkey1 type: speeddial
softkey1 value: {{ exten_voicemail }}
softkey1 label: "{{ XX_dict['voicemail'] }}"
{% endif -%}

{% if exten_fwd_unconditional -%}
softkey2 type: speeddial
softkey2 value: {{ exten_fwd_unconditional }}
softkey2 label: "{{ XX_dict['fwd_unconditional'] }}"
{% endif -%}

{% if exten_dnd -%}
softkey3 type: speeddial
softkey3 value: {{ exten_dnd }}
softkey3 label: "{{ XX_dict['dnd'] }}"
{% endif -%}

{% include 'base.tpl' %}

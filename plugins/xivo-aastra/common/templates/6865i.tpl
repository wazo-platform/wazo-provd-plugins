prgkey5 locked: 0

prgkey6 locked: 0

{% if XX_xivo_phonebook_url -%}
prgkey5 type: none
prgkey6 type: none
directory script: {{ XX_xivo_phonebook_url }}
{% endif -%}

{% if exten_voicemail -%}
prgkey1 type: speeddial
prgkey1 value: {{ exten_voicemail }}
prgkey1 label: "{{ XX_dict['voicemail'] }}"
{% endif -%}

{% if exten_fwd_unconditional -%}
prgkey2 type: speeddial
prgkey2 value: {{ exten_fwd_unconditional }}
prgkey2 label: "{{ XX_dict['fwd_unconditional'] }}"
{% endif -%}

{% if exten_dnd -%}
prgkey3 type: speeddial
prgkey3 value: {{ exten_dnd }}
prgkey3 label: "{{ XX_dict['dnd'] }}"
{% endif -%}

{% include 'base.tpl' %}

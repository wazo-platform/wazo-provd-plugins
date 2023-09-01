idle screen mode: 1

date format: 8

sip stun ip: stun.wazo.io

play a ring splash: 0

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

softkey4 type: directory
softkey4 label: "Wazo"

{% if XX_xivo_phonebook_url -%}
directory script: {{ XX_xivo_phonebook_url }}
{% endif -%}

{% include 'base.tpl' %}

{% if exten_voicemail -%}
topsoftkey1 type: speeddial
topsoftkey1 value: {{ exten_voicemail }}
topsoftkey1 label: "{{ XX_dict['voicemail'] }}"
{% endif -%}

{% if exten_fwd_unconditional -%}
topsoftkey2 type: speeddial
topsoftkey2 value: {{ exten_fwd_unconditional }}
topsoftkey2 label: "{{ XX_dict['fwd_unconditional'] }}"
{% endif -%}

{% if exten_dnd -%}
topsoftkey3 type: speeddial
topsoftkey3 value: {{ exten_dnd }}
topsoftkey3 label: "{{ XX_dict['dnd'] }}"
{% endif -%}

topsoftkey4 type: directory
topsoftkey4 label: "{{ XX_dict['local_directory'] }}"

topsoftkey5 type: callers
topsoftkey5 label: "{{ XX_dict['callers'] }}"

topsoftkey6 type: services
topsoftkey6 label: "{{ XX_dict['services'] }}"

{% if exten_pickup_call -%}
topsoftkey7 type: speeddial
topsoftkey7 value: {{ exten_pickup_call }}
topsoftkey7 label: "{{ XX_dict['pickup_call'] }}"
{% endif -%}

{% if X_xivo_phonebook_ip -%}
softkey1 type: xml
softkey1 value: https://{{ X_xivo_phonebook_ip }}/service/ipbx/web_services.php/phonebook/search/
softkey1 label: "{{ XX_dict['remote_directory'] }}"
{% endif -%}

{% include 'base.tpl' %}

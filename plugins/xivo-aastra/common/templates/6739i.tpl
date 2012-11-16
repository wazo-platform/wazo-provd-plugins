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

{% if X_xivo_phonebook_ip -%}
softkey3 type: xml
softkey3 label: "{{ XX_dict['remote_directory'] }}"
softkey3 value: https://{{ X_xivo_phonebook_ip }}/service/ipbx/web_services.php/phonebook/search/
{% endif -%}

{% include 'base.tpl' %}

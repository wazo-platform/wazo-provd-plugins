prgkey5 locked: 0

prgkey6 locked: 0

{% if X_xivo_phonebook_ip -%}
prgkey5 type: none
prgkey6 type: none
directory script: http://{{ X_xivo_phonebook_ip }}/service/ipbx/web_services.php/phonebook/search/
{% endif -%}

{% include 'base.tpl' %}

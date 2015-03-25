{% if X_xivo_phonebook_ip -%}
topsoftkey1 type: xml
topsoftkey1 value: http://{{ X_xivo_phonebook_ip }}/service/ipbx/web_services.php/phonebook/search/
{% endif -%}

{% include 'base.tpl' %}

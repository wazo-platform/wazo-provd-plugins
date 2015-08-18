topsoftkey1 type: directory

{% if X_xivo_phonebook_ip -%}
directory script: http://{{ X_xivo_phonebook_ip }}/service/ipbx/web_services.php/phonebook/search/
{% endif -%}

{% include 'base.tpl' %}

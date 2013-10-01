{% extends 'base.tpl' %}

{% block fkeys_prefix %}
{% if X_xivo_phonebook_ip %}
<fkey idx="4" context="active" perm="R">url http://{{ X_xivo_phonebook_ip }}/service/ipbx/web_services.php/phonebook/search/</fkey>
{% endif %}
{% endblock %}

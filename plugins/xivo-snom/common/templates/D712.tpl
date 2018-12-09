{% extends 'base.tpl' %}

{% block fkeys_prefix %}
{% if XX_xivo_phonebook_url %}
    <fkey idx="4" context="active" perm="R">url {{ XX_xivo_phonebook_url|e }}</fkey>
{% endif %}
{% endblock %}

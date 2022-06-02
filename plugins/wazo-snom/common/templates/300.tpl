{% extends 'base.tpl' %}

{% block fkeys_prefix %}
<fkey idx="0" context="1" perm="R">line</fkey>
<fkey idx="1" context="2" perm="R">line</fkey>
<fkey idx="2" context="active" perm="R">keyevent F_REDIAL</fkey>
{% if XX_xivo_phonebook_url -%}
<fkey idx="3" context="active" perm="R">none</fkey>
{% else -%}
<fkey idx="3" context="active" perm="R">keyevent F_ADR_BOOK</fkey>
{% endif -%}
<fkey idx="4" context="active" perm="R">transfer</fkey>
<fkey idx="5" context="active" perm="R">keyevent F_MUTE</fkey>
{% endblock %}

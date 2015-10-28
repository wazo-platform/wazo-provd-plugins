{% extends 'base.tpl' -%}

{% block gui_fkey1 %}{% endblock %}

{% block settings_suffix %}
<!-- since firmware 8.7.5.17 for D765 is not available, prevent error messages from
     being displayed by setting update_policy to settings_only -->
<update_policy perm="R">settings_only</update_policy>
<gui_fkey1 perm="R">F_ADR_BOOK</gui_fkey1>
<gui_fkey4 perm="R">none</gui_fkey4>
{% endblock %}

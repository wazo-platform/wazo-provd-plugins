{% extends 'base.tpl' -%}

{# Classic-generation hardware: shipped only by the 8.7.5.35 / 8.9.3.80
   plugins, never by a 10.1.x one. Kept on gui_fkey1 because context_key
   is a D-series/10.x setting these phones do not parse. #}
{% block gui_fkey %}{% endblock %}

{% block settings_suffix %}
{% if XX_xivo_phonebook_url -%}
<gui_fkey1 perm="R">none</gui_fkey1>
{% else -%}
<gui_fkey1 perm="R">F_ADR_BOOK</gui_fkey1>
{% endif -%}
<gui_fkey4 perm="R">none</gui_fkey4>
{% endblock %}

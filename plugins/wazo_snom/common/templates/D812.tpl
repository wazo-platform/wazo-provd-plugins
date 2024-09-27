{% extends 'base.tpl' -%}

{% block gui_fkey1 %}{% endblock %}

{% block settings_suffix %}
{% if XX_xivo_phonebook_url -%}
<gui_fkey4 perm="R">keyevent F_NONE</gui_fkey4>
{% else -%}
<gui_fkey4 perm="R">keyevent F_ADR_BOOK</gui_fkey4>
<context_key idx="3" perm="">url {{ XX_xivo_phonebook_url|e }}</context_key>
<context_key_label idx="3" perm="">{{ XX_dict['remote_directory'] }}</context_key_label>
{% endif -%}
{% endblock %}

{% extends 'base.tpl' -%}

{% block gui_fkey %}
<gui_fkey1 perm="R">
    <initialization>
        <variable name="label" value="{{ XX_dict['remote_directory'] }}"/>
        <variable name="icon" value="kIconTypeFkeyAdrBook"/>
    </initialization>
    <action>
        <url target="{{ XX_xivo_phonebook_url|e }}" when="on press"/>
    </action>
</gui_fkey1>
<context_key idx="2" perm="RW">redirect </context_key>
<context_key idx="3" perm="R">keyevent F_SETTINGS</context_key>
{% endblock %}

{% block settings_suffix %}
<locale perm="RW">{{ XX_locale|e }}</locale>
{% endblock %}

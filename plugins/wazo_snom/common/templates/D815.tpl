{% extends 'base.tpl' -%}

{% block gui_fkey %}
<gui_fkey3 perm="R">
    <initialization>
        <variable name="label" value="{{ XX_dict['remote_directory'] }}"/>
    </initialization>
    <action>
        <url target="{{ XX_xivo_phonebook_url|e }}" when="on press"/>
        <variable name="icon" value="kIconTypeFkeyAdrBook"/>
    </action>
</gui_fkey3>
{% endblock %}

{% block settings_suffix %}
<locale perm="PERMISSIONFLAG">{{ XX_locale|e }}</locale>
{% endblock %}

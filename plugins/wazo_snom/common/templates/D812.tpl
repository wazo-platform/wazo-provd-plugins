{% extends 'base.tpl' -%}

{% block settings_suffix %}
    <gui_fkey4 perm="R">
        <initialization>
            <variable name="label" value="{{ XX_dict['remote_directory'] }}"/>
        </initialization>
        <action>
            <url target="{{ XX_xivo_phonebook_url|e }}" when="on press"/>
        </action>
    </gui_fkey4>
{% endblock %}

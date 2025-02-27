{% extends 'base-new.tpl' %}
{% block model_specific_parameters -%}
    {% if XX_xivo_phonebook_url -%}
        <dssSoft index="1">
            <Type>21</Type>
            <Value>{{ XX_xivo_phonebook_url }}</Value>
            <Title>{{ XX_directory|d('Directory') }}</Title>
        </dssSoft>
    {%- endif %}
{% endblock %}

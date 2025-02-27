{% include 'base.tpl' %}
{% block model_specific_parameters -%}
    {% if XX_wazo_phonebook_url_v2 -%}
        <dssSoft index="1">
            <Type>21</Type>
            <Value>{{ XX_wazo_phonebook_url_v2 }}</Value>
            <Title>{{ XX_directory|d('Directory') }}</Title>
        </dssSoft>
    {%- endif %}
{% endblock %}

{% extends 'base-w-series.tpl' %}

{% block model_specific_fkeys -%}
    <dsskey>
        {% if XX_paginated_fkeys -%}
        {% for page, index, fkey in XX_paginated_fkeys -%}
        {% if page == 1 -%}
        <dssSoft index="{{ index }}">
                <Type>{{ fkey['type'] }}</Type>
                <Value>{{ fkey['value'] }}</Value>
                <Title>{{ fkey['title'] }}</Title>
        </dssSoft>
        {% endif -%}
        {% if page == 2 -%}
        <internal index="1">
            <Fkey index="{{ index }}">
                <Type>{{ fkey['type'] }}</Type>
                <Value>{{ fkey['value'] }}</Value>
                <Title>{{ fkey['title'] }}</Title>
            </Fkey>
        </internal>
        {% endif -%}
        {%- endfor %}
        {% endif -%}
    </dsskey>
{% endblock %}

{% block model_specific_parameters -%}
{% endblock %}

{% extends 'base-w-series.tpl' %}

{% block model_specific_fkeys -%}
    <dsskey>
        {% if XX_paginated_fkeys -%}
        {% for page, index, fkey in XX_paginated_fkeys -%}
        <internal index="{{ page }}">
            <Fkey index="{{ index }}">
                <Type>{{ fkey['type'] }}</Type>
                <Value>{{ fkey['value'] }}</Value>
                <Title>{{ fkey['title'] }}</Title>
            </Fkey>
        </internal>
        {%- endfor %}
        {% endif -%}
    </dsskey>
{% endblock %}

{% block model_specific_parameters -%}
{% endblock %}

{% extends 'base-i-series.tpl' %}

{% block model_specific_fkeys -%}
    <dsskey>
        {% if XX_paginated_fkeys -%}
            <FuncKeyPageNum>{{ XX_max_page }}</FuncKeyPageNum>
        {% for page, index, fkey in XX_paginated_fkeys -%}
        {% if loop.index0 == 0 or page != loop.previtem[0] -%}
        {% if loop.index0 != 0 -%}
        </internal>
        {%- endif %}
        <internal index="{{ page + 1 }}">
        {%- endif %}
            <Fkey index="{{ index }}">
                <Type>{{ fkey['type'] }}</Type>
                <Value>{{ fkey['value'] }}</Value>
                <Title>{{ fkey['title'] }}</Title>
            </Fkey>
        {%- endfor %}
        </internal>
        {% endif -%}

    </dsskey>
{% endblock %}

{% block model_specific_parameters -%}
{% endblock %}

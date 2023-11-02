{% extends 'base-i-series.tpl' %}

{% block model_specific_fkeys -%}
    <dsskey>
        {% if XX_paginated_fkeys -%}
        {% for page, index, fkey in XX_paginated_fkeys -%}
        <dssSoft index="{{ index }}">
                <Type>{{ fkey['type'] }}</Type>
                <Value>{{ fkey['value'] }}</Value>
                <Title>{{ fkey['title'] }}</Title>
        </dssSoft>

        {%- endfor %}
        {% endif -%}
    </dsskey>
{% endblock %}

{% block model_specific_parameters -%}
<sip>
<line index="1">
<AutoAnswer>1</AutoAnswer>
</line>
</sip>
{% endblock %}

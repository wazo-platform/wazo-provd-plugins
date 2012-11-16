{% extends 'base.tpl' %}

{% block upgrade_rule %}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/firmware/spa8000-6-1-3.bin</Upgrade_Rule>
{% endblock %}

{% block suffix %}
{% endblock %}

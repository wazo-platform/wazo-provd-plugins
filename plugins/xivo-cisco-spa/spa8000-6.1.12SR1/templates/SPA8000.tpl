{% extends 'base.tpl' %}

{% block upgrade_rule %}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/firmware/spa8000-6-1-12-SR1.bin?mac=$MA</Upgrade_Rule>
{% endblock %}

{% block suffix %}
{% endblock %}

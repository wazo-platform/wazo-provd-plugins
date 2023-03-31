{% extends 'base.tpl' %}

{% block upgrade_rule %}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/firmware/spa941-5-1-8.bin</Upgrade_Rule>
{% endblock %}

{% block suffix %}
{% endblock %}

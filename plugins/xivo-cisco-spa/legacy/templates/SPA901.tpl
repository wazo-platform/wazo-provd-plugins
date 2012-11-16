{% extends 'base.tpl' %}

{% block upgrade_rule %}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/firmware/spa901-5-1-5.bin</Upgrade_Rule>
{% endblock %}

{% block suffix %}
{% endblock %}

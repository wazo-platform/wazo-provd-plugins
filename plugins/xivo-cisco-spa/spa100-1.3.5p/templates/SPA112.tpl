{% extends 'base.tpl' %}

{% block upgrade_rule %}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/firmware/SPA112-SPA122_1.4.1.bin</Upgrade_Rule>
{% endblock %}

{% block suffix %}
{% endblock %}

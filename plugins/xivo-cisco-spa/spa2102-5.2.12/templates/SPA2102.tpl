{% extends 'base.tpl' %}

{% block upgrade_rule %}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/firmware/spa2102-5-2-12.bin</Upgrade_Rule>
{% endblock %}

{% block suffix %}
{% endblock %}

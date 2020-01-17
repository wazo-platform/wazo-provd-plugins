{% extends 'base.tpl' %}

{% block upgrade_rule %}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/firmware/spa3102-5-1-10-GW.bin?mac=$MA</Upgrade_Rule>
{% endblock %}

{% block suffix %}
{% endblock %}

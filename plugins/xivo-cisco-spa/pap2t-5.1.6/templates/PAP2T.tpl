{% extends 'base.tpl' %}

{% block upgrade_rule %}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/firmware/pap2t-5-1-6.bin</Upgrade_Rule>
{% endblock %}

{% block suffix %}
{% endblock %}

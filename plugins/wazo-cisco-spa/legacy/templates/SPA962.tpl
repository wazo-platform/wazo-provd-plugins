{% extends 'base.tpl' %}

{% block upgrade_rule %}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/firmware/spa962-6-1-5a.bin</Upgrade_Rule>
{% endblock %}

{% block dictionary_server_script %}
<Dictionary_Server_Script>serv=http://{{ ip }}:{{ http_port }}/i18n/;d0=English;x0=enS.xml;d1=French;x1=frS.xml;d2=German;x2=deS.xml;d3=Spanish;x3=esS.xml</Dictionary_Server_Script>
{% endblock %}

{% block suffix %}
{% endblock %}

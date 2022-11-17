{% extends 'base.tpl' %}

{% block upgrade_rule %}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/firmware/spa525g-7-5-5.bin</Upgrade_Rule>
{% endblock %}

{% block dictionary_server_script %}
<Dictionary_Server_Script>serv=http://{{ ip }}:{{ http_port }}/i18n/;d0=English;x0=spa525_en_v755.xml;d1=French;x1=spa525_fr_v755.xml;d2=German;x2=spa525_de_v755.xml;d3=Spanish;x3=spa525_es_v755.xml</Dictionary_Server_Script>
{% endblock %}

{% block suffix %}
{% endblock %}

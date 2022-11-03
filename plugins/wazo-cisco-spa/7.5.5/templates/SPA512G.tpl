{% extends 'base.tpl' %}

{% block upgrade_rule %}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/firmware/spa51x-7-5-5.bin</Upgrade_Rule>
{% endblock %}

{% block dictionary_server_script %}
<Dictionary_Server_Script>serv=http://{{ ip }}:{{ http_port }}/i18n/;d0=English;x0=spa50x_30x_en_v755.xml;d1=French;x1=spa50x_30x_fr_v755.xml;d2=German;x2=spa50x_30x_de_v755.xml;d3=Spanish;x3=spa50x_30x_es_v755.xml</Dictionary_Server_Script>
{% endblock %}

{% block suffix %}
{% endblock %}

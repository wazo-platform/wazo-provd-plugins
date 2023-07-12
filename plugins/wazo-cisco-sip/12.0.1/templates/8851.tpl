{% extends 'base.tpl' -%}

{% block upgrade_rule -%}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/sip88xx.12-0-1MPP0001-245.loads</Upgrade_Rule>
{% endblock -%}

{% block dictionary_server_script %}
<Dictionary_Server_Script>serv=http://{{ ip }}:{{ http_port }}/locales/;d0=English;x0=en-US_88xx-12.0.1.1000.xml;d1=French;x1=fr-FR_88xx-12.0.1.1000.xml;d2=German;x2=de-DE_88xx-12.0.1.1000.xml;d3=Spanish;x3=es-ES_88xx-12.0.1.1000.xml</Dictionary_Server_Script>
{% endblock %}

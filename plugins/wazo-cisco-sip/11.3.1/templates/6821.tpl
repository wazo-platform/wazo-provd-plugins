{% extends 'base.tpl' -%}

{% block dictionary_server_script %}
<Dictionary_Server_Script>serv=http://{{ ip }}:{{ http_port }}/locales/;d0=English;x0=en-US_6821-11.3.2.1000.xml;d1=French;x1=fr-FR_6821-11.3.2.1000.xml;d2=German;x2=de-DE_6821-11.3.2.1000.xml;d3=Spanish;x3=es-ES_6821-11.3.2.1000.xml</Dictionary_Server_Script>
{% endblock %}

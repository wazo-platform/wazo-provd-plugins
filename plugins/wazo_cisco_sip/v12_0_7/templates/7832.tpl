{% extends 'base.tpl' -%}

{% block upgrade_rule -%}
<Upgrade_Rule>{{ XX_server_url }}/sip78xx.12-0-7MPP0201-66.loads</Upgrade_Rule>
{% endblock -%}

{% block dictionary_server_script %}
<Dictionary_Server_Script>serv={{ XX_server_url }}/locales/;d0=English;x0=en-US_88xx-12.0.4.0002.xml;d1=French;x1=fr-FR_88xx-12.0.4.0002.xml;d2=German;x2=de-DE_88xx-12.0.4.0002.xml;d3=Spanish;x3=es-ES_88xx-12.0.4.0002.xml</Dictionary_Server_Script>
{% endblock %}

{% extends 'base.tpl' -%}

{% block upgrade_rule -%}
<Upgrade_Rule>{{ XX_server_url }}/sip68xx.11-3-1MSR3-3.loads</Upgrade_Rule>
{% endblock -%}

{% block dictionary_server_script %}
<Dictionary_Server_Script>serv={{ XX_server_url }}/locales/;d0=English;x0=en-US_78xx_68xx-11.3.2.1000.xml;d1=French;x1=fr-FR_78xx_68xx-11.3.2.1000.xml;d2=German;x2=de-DE_78xx_68xx-11.3.2.1000.xml;d3=Spanish;x3=es-ES_78xx_68xx-11.3.2.1000.xml</Dictionary_Server_Script>
{% endblock %}

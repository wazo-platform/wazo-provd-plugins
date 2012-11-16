{% extends 'base.tpl' %}

{% block upgrade_rule %}
<Upgrade_Rule>http://{{ ip }}:{{ http_port }}/firmware/spa50x-30x-7-4-8a.bin</Upgrade_Rule>
{% endblock %}

{% block dictionary_server_script %}
<Dictionary_Server_Script>serv=http://{{ ip }}:{{ http_port }}/i18n/;d0=English;x0=spa50x_30x_en.xml;d1=French;x1=spa50x_30x_fr.xml;d2=German;x2=spa50x_30x_de.xml;d3=Spanish;x3=spa50x_30x_es.xml</Dictionary_Server_Script>
{% endblock %}

{% block suffix %}
<Dial_Plan_1_>([x*].)</Dial_Plan_1_>
<Dial_Plan_2_>([x*].)</Dial_Plan_2_>
<Dial_Plan_3_>([x*].)</Dial_Plan_3_>
<Dial_Plan_4_>([x*].)</Dial_Plan_4_>
<Dial_Plan_5_>([x*].)</Dial_Plan_5_>
<Dial_Plan_6_>([x*].)</Dial_Plan_6_>
<Dial_Plan_7_>([x*].)</Dial_Plan_7_>
<Dial_Plan_8_>([x*].)</Dial_Plan_8_>
{% endblock %}

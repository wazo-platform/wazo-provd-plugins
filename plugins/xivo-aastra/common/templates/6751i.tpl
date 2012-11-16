{% include 'base.tpl' %}

{# sip lineN vmail is not understood by the 6751i -#}
{% if exten_voicemail -%}
sip vmail: {{ exten_voicemail }}
{% endif -%}

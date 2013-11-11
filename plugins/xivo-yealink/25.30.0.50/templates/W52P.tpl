{% include 'base.tpl' -%}

{% for line in sip_lines.itervalues() %}
handset.{{ line['XX_line_no'] }}.name = {{ line['display_name'] }}
handset.{{ line['XX_line_no'] }}.incoming_lines = {{ line['XX_line_no'] }}
handset.{{ line['XX_line_no'] }}.dial_out_default_line = {{ line['XX_line_no'] }}
handset.{{ line['XX_line_no'] }}.dial_out_lines = {{ line['XX_line_no'] }}
{% endfor -%}

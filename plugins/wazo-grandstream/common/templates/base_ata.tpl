{% extends 'base.tpl' -%}
{% block model_specific_config -%}
{# Fax-specific -#}
{# Caller ID Scheme.
# <value=0>  Bellcore/Telcordia (default)
# <value=1>  ETSI-FSK during ringing
# <value=2>  ETSI-FSK prior to ringing with DTAS
# <value=3>  ETSI-FSK prior to ringing with LR+DTAS
# <value=4>  ETSI-FSK prior to ringing with RP
# <value=5>  ETSI-DTMF during ringing
# <value=6>  ETSI-DTMF prior to ringing with DTAS
# <value=7>  ETSI-DTMF prior to ringing with LR+DTAS
# <value=8>  ETSI-DTMF prior to ringing with RP
# <value=9>  SIN 227 - BT
# <value=10> NTT Japan
# <value=11> DTMF Denmark prior to ringing no DTAS no LR
# <value=12> DTMF Denmark prior to ringing with LR
# <value=13> DTMF Sweden/Finalnd prior to ringing with LR
# <value=14> DTMF Brazil
# Number: 0 to 14
# Mandatory -#}
<P863>0</P863>
{# SLIC Setting.
# 0 - USA (BELLCORE 600 ohms), 3 - USA 2(BELCORE 600 ohms + 2.16uF), 11 - AUSTRAILA, 5 - CHINA CO, 6 - CHINA PBX, 4 - EUROPEAN CTR21
# 9 - GERMANY, 8 -INDIA/NEW ZEALAND, 2 - JAPAN CO, 7 - JAPAN PBX, 1 - STANDARD 900 omhs, 10 - UK
# Number: 0-11
# Mandatory -#}
<P854>3</P854>
{# FAX Mode. 0 - T.38 (Auto Detect), 1 - Pass Through
# Number: 0, 1
# Mandatory -#}
<P228>0</P228>
{# Re-INVITE After Fax Tone Detected. 0 - Disabled, 1 - Enabled.
# Number: 0, 1
# Mandatory -#}
<P4417>1</P4417>
{% endblock -%}

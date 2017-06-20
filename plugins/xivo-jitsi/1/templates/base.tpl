{% for line_no, line in sip_lines.iteritems() %}
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}=acc{{ line_no }}
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.ACCOUNT_UID=SIP\:{{ line['username'] }}@{{ line['proxy_ip'] or sip_proxy_ip }}
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.AUTHORIZATION_NAME={{ line['auth_username'] }}
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.DEFAULT_ENCRYPTION=true
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.DEFAULT_SIPZRTP_ATTRIBUTE=true
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.DISPLAY_NAME={{ line['display_name'] }}
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.FORCE_P2P_MODE=false
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.IS_PRESENCE_ENABLED=false
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.KEEP_ALIVE_INTERVAL=25
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.KEEP_ALIVE_METHOD=NONE
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.POLLING_PERIOD=30
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.PASSWORD={{ line['password'] }}
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.PROTOCOL_NAME=SIP
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.PROXY_ADDRESS_VALIDATED=true
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.PROXY_AUTO_CONFIG=true
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.SERVER_ADDRESS={{ line['proxy_ip'] or sip_proxy_ip }}
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.SERVER_ADDRESS_VALIDATED=true
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.SERVER_PORT={{ line['proxy_port'] or sip_proxy_port|d(5060) }}
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.SUBSCRIPTION_EXPIRATION=3600
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.USER_ID={{ line['username'] }}@{{ line['proxy_ip'] or sip_proxy_ip }}
net.java.sip.communicator.impl.protocol.sip.acc{{ line_no }}.XCAP_ENABLE=false
{% endfor -%}

SET ENABLE_WEBSERVER 1
{% if admin_password -%}
SET FORCE_WEB_ADMIN_PASSWORD {{ admin_password }}
{% endif -%}
SET CODEC_PRIORITY G711A,G711U,G722
SET ENABLE_G729 0
SET ENABLE_G726 0
SET ENABLE_OPUS 0
SET ENHDIALSTAT 0
SET ENABLE_AVAYA_ENVIRONMENT 0
SET DISCOVER_AVAYA_ENVIRONMENT 0
SET ENABLE_3PCC_ENVIRONMENT 1
SET ENCRYPT_VERSION_IN_USE 1
SET MAX__DISPLAYED_SESSION_APPEARANCES 3
SET COUNTRY FR
SET INPUT_METHOD 3
SET DSTOFFSET 2
SET REG_DATE_HEADER 1718640719
SET DATEFORMAT %d/%m
SET ADMINTIMEFORMAT 1
{% if ip -%}
SET HTTPUSED {{ ip }}
SET HTTPSRVR {{ ip }}
SET HTTPSRVR_IN_USE {{ ip }}
{% endif -%}
{% if http_port -%}
SET HTTPPORT {{ http_port }}
{% endif -%}
SET CHECK_FILE_SERVER 0
{% if ntp_enabled -%}
SET SNTPSRVR {{ ntp_ip }}
SET SNTPSRVR_IN_USE {{ ntp_ip }}
{% endif -%}
SET TRUSTLIST 1
SET APP_DOWNLOAD_STATUS 14
SET RESTART_COUNTER 4
SET PHY1_OPERATIONAL_MODE 5
SET TIMEZONE Europe/Paris
{% if '1' in sip_lines -%}
{% set line = sip_lines['1'] -%}
{% set proxy_ip = line['proxy_ip'] or sip_proxy_ip -%}
SET SIPSIGNAL 0
SET SIPPROXYSRVR {{ proxy_ip }}
SET SIP_CONTROLLER_MODE 1
SET SIP_CONTROLLER_LIST {{ proxy_ip }}:{{ line['proxy_port'] }};transport=udp
SET SIPPROXYSRVR_IN_USE {{ proxy_ip }}
SET SIP_PROXY_SELECTION_POLICY 1
SET SIPDOMAIN {{ proxy_ip }}
SET MWISRVR {{ proxy_ip }}
SET USER_LOGGED_IN 1
SET DISPLAY_NAME {{ line['display_name'] }}
SET SIP_USER_ACCOUNT {{ line['username'] }}@{{ proxy_ip }}
SET SIP_USER_ID {{ line['auth_username'] }}
SET PREV_SIP_USER_ACCOUNT {{ line['username'] }}@{{ proxy_ip }}
SET FORCE_SIP_USERNAME "{{ line['auth_username'] }}"
SET FORCE_SIP_PASSWORD "{{ line['password'] }}"
SET FORCE_SIP_EXTENSION "{{ line['auth_username'] }}"
SET ENABLE_SIP_USER_ID 1
{% endif -%}

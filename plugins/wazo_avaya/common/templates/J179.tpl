SET ENABLE_WEBSERVER 1
{% if admin_password -%}
SET FORCE_WEB_ADMIN_PASSWORD {{ admin_password }}
{% endif -%}
SET CODEC_PRIORITY G711A,G711U,G722
SET ENABLE_G729 0
SET ENABLE_G726 0
SET ENABLE_OPUS 0
SET ENCRYPT_VERSION_IN_USE 1
SET MAX__DISPLAYED_SESSION_APPEARANCES 3
SET LANGUAGE_FILE_IN_USE Mlf_J169_J179_ParisianFrench.xml
SET LANGUAGES_RESOURCE_LIST English=res://Mlf_English.xml,Parisian French=lang/Mlf_J169_J179_ParisianFrench.xml
SET SYSTEM_LANGUAGE Mlf_J169_J179_ParisianFrench.xml
SET LANGUAGE_IN_USE Parisian French
SET LANGUAGES firmware/Mlf_J169_J179_ParisianFrench.xml
SET INPUT_METHOD 3
SET REG_DATE_HEADER 1718640719
SET DATEFORMAT %d/%m
SET HTTPUSED {{ XX_server_url_without_port }}
SET HTTPSRVR {{ XX_server_url_without_port }}
SET HTTPSRVR_IN_USE {{ XX_server_url_without_port }}
SET HTTPPORT {{ XX_server_url_port }}
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
SET SIP_CONTROLLER_LIST {{ proxy_ip }}:{{ proxy_port }};transport=udp
SET SIPPROXYSRVR_IN_USE {{ proxy_ip }}
SET SIP_PROXY_SELECTION_POLICY 1
SET SIPDOMAIN {{ proxy_ip }}
SET MWISRVR {{ proxy_ip }}
SET USER_LOGGED_IN 1
SET DISPLAY_NAME Wazo
SET SIP_USER_ACCOUNT {{ line['username'] }}@{{ proxy_ip }}
SET SIP_USER_ID {{ line['auth_username'] }}
SET PREV_SIP_USER_ACCOUNT {{ line['username'] }}@{{ proxy_ip }}
SET FORCE_SIP_USERNAME "{{ line['auth_username'] }}"
SET FORCE_SIP_PASSWORD "{{ line['password'] }}"
SET FORCE_SIP_EXTENSION "{{ line['auth_username'] }}"
SET ENABLE_SIP_USER_ID 1
{% endif -%}
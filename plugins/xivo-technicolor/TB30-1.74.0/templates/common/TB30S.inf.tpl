[application]
fwurl=http://{{ ip }}:{{ http_port }}/binary/TB30S.R11.101217.1.74.0.zz
dspurl=http://{{ ip }}:{{ http_port }}/binary/TB30S_V2.30.1_dsp.zz
booturl=http://{{ ip }}:{{ http_port }}/binary/TB30S_BOOT_V1.02.0.0.zz

[config]
telcfg=http://{{ ip }}:{{ http_port }}/telconf-1.74.0-1.txt
common_config=http://{{ ip }}:{{ http_port }}/comconf-1.74.0-1.txt
config=http://{{ ip }}:{{ http_port }}/


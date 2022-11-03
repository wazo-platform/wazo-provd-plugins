[application]
fwurl=http://{{ ip }}:{{ http_port }}/binary/v2022SG.R11.1.SED.120313.4.78.1.zz
dspurl=http://{{ ip }}:{{ http_port }}/binary/v2022_dsp_R11.1_SED_v320.zz
booturl=http://{{ ip }}:{{ http_port }}/binary/v2022_boot_v303.zz

[config]
telcfg=http://{{ ip }}:{{ http_port }}/telconf-4.78.1-1.txt
common_config=http://{{ ip }}:{{ http_port }}/comconf-4.78.1-1.txt
config=http://{{ ip }}:{{ http_port }}/


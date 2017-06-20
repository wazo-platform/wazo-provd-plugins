[application]
fwurl=http://{{ ip }}:{{ http_port }}/binary/v2030SG.R11.1.SED.101223.2.74.zz
dspurl=http://{{ ip }}:{{ http_port }}/binary/v2030_dsp_R11.1_SED_v320.zz
booturl=http://{{ ip }}:{{ http_port }}/binary/v2030_boot_v111.zz

[config]
telcfg=http://{{ ip }}:{{ http_port }}/telconf-2.74-1.txt
common_config=http://{{ ip }}:{{ http_port }}/comconf-2.74-1.txt
config=http://{{ ip }}:{{ http_port }}/


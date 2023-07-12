<?xml version="1.0" standalone="yes"?>
<flat-profile>
<Resync_On_Reset ua="na">Yes</Resync_On_Reset>
<Resync_Periodic ua="na">3600</Resync_Periodic>
<Profile_Rule ua="na">http://{{ ip }}:{{ http_port }}/ata$PSN.cfg</Profile_Rule>
<Profile_Rule_B ua="na">http://{{ ip }}:{{ http_port }}/spa-ata.xml?mac=$MA</Profile_Rule_B>
<Profile_Rule_C ua="na">http://{{ ip }}:{{ http_port }}/$MA.xml</Profile_Rule_C>
</flat-profile>

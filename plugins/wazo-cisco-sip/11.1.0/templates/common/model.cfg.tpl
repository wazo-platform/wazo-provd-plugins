<?xml version="1.0" standalone="yes"?>
<flat-profile>
<Resync_On_Reset>Yes</Resync_On_Reset>
<Resync_Periodic>3600</Resync_Periodic>
<Profile_Rule_B>http://{{ ip }}:{{ http_port }}/spa-ata.xml?mac=$MA</Profile_Rule_B>
<Profile_Rule_C>http://{{ ip }}:{{ http_port }}/$MA.xml</Profile_Rule_C>
</flat-profile>

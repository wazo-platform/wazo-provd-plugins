<?xml version="1.0" encoding="UTF-8" ?>
<VOIP_CONFIG_FILE>
<version>2.0002</version>
<AUTOUPDATE_CONFIG_MODULE>
<Download_Username></Download_Username>
<Download_Password></Download_Password>
<Download_Server_IP>{{ ip }}</Download_Server_IP>
<Config_File_Name>Fanvil/$mac.cfg</Config_File_Name>
<Config_File_Key></Config_File_Key>
<Common_Cfg_File_Key></Common_Cfg_File_Key>
<Download_Protocol>2</Download_Protocol>
<Download_Mode>1</Download_Mode>
<Download_Interval>1</Download_Interval>
<DHCP_Option>66</DHCP_Option>
<PNP_Enable>0</PNP_Enable>
<Auto_Image_URL>http://{{ ip }}:{{ http_port }}/Fanvil/firmware/{{ XX_fw_filename }}</Auto_Image_URL>
<Save_Provision_Info>1</Save_Provision_Info>
</AUTOUPDATE_CONFIG_MODULE>
<<END OF FILE>>

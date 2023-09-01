{% include 'base.tpl' %}

profile provisioning PF_PROVISIONING_FIRMWARE
  destination script
  location 1 $(dhcp.66)/sn4300/bw
  activation reload graceful


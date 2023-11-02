profile call-progress-tone FR_Dialtone
  play 1 5000 440 -10

profile call-progress-tone FR_Alertingtone
  play 1 1500 440 -10
  pause 2 3500

profile call-progress-tone FR_Busytone
  play 1 500 440 -10
  pause 2 500

profile tone-set default
  map call-progress-tone dial-tone FR_Dialtone
  map call-progress-tone ringback-tone FR_Alertingtone
  map call-progress-tone busy-tone FR_Busytone
  map call-progress-tone release-tone FR_Busytone
  map call-progress-tone congestion-tone FR_Busytone

profile voip default
  codec 1 g711alaw64k rx-length 20 tx-length 20
  codec 2 g711ulaw64k rx-length 20 tx-length 20
  dtmf-relay {{ XX_dtmf_relay|d('default') }}
  ced net-side-detection
  fax transmission 1 relay t38-udp
  fax transmission 2 bypass g711alaw64k rx-length 20 tx-length 20

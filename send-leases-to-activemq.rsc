#-------------------------------------------------------------------------------
# MikroTik RouterOS Send Leases to ActiveMQ
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------------------
:local ACTIVEMQHOST "activemq.tld"
:local ACTIVEMQPORT 8161
:local ACTIVEMQUSER "admin"
:local ACTIVEMQPASSWORD "admin"
:local ACTIVEMQTOPIC "leases"

#-------------------------------------------------------------------------------
# Send Leases to ActiveMQ
#-------------------------------------------------------------------------------
:local url "http://$ACTIVEMQHOST:$ACTIVEMQPORT/api/message/$ACTIVEMQTOPIC"
:local date [/system clock get date]
:local time [/system clock get time]
:local message "{\"date\":\"$date\",\"time\":\"$time\",\"bound\":$leaseBound,\"serverName\":\"$leaseServerName\",\"mac\":\"$leaseActMAC\",\"ip\":\"$leaseActIP\"}"
/tool fetch url="$url" http-method="post" user="$ACTIVEMQUSER" password="$ACTIVEMQPASSWORD" http-data="body=$message" keep-result="no"

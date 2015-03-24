IQinvision Dynamic Print (DP) variables
=======================================
Variable | Description
------------- | -------------
$SH | Your camera’s hardware address.
$SI | Your camera’s IP address.
$SN | Your camera’s name, as specified on the Network Settings page.
$ST | The current time (in 24-hour format: HH:MM:SS, ex: 16:05:20).
$SD | The current date (ex: Wed Feb 03 2010).
$SC | Company name (e.g. IQinVision).
$SP | Product name (e.g. IQeye752).
$SV | The version of operating software on your camera.
$SM | The domain name, as specified on the Network Settings page.
$FN | The name of the file that your camera is accessing.
$MSE | Milliseconds since epoch
$IMGDBG | Image debug data
$O(oidNumber) | Display an OID, like IP address (3.6.10) or the image focus value(1.2.25) or last trigger event time (1.3.20). Use http://<yourcameraip>/oidtable.html to see all available OIDs.

For time-based variables, you can use $SD in combination with the common strftime() UNIX time variables.

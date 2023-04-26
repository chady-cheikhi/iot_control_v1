#!/bin/bash
state=0
while [ $state -ne 1 ];do
state=$(nmcli connection show --active |grep GPSA | grep -v
not | wc -l)
if [ $state -eq 1 ]
then
sleep 3m
firefox
http://10.106.134.210:8080/d/lpU4hW3Mz/dashboard-montage2?orgId=1&refresh=1m&kiosk &
xdotool search --sync --onlyvisible --class "Firefox"
windowactivate key F11
else
cd ~/Desktop
nmcli connection up GPSA 2>&1 | tee -a
~/Desktop/rapport/connexion.log
fi
done
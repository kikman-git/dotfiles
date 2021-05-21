#!/usr/bin/env bash
set -euo pipefail

# picom --experimental-backends &
dunst &
unclutter &
# bluetoothctl power off &
# blueberry-tray &
# greenclip daemon &
#idle.sh 7 screensaver &
#light-locker --lock-after-screensaver=0 --no-lock-on-suspend --no-lock-on-lid --no-idle-hint &
~/.fehbg &
xidlehook --not-when-fullscreen --not-when-audio --timer 420 'screensaver' '' --timer 180 'xset dpms force off; lockscreen.sh' '' &
# flashfocus &
mkfifo /tmp/vol && echo "$(pulsemixer --get-volume | awk '{print $1}')" > /tmp/vol & 
mkfifo /tmp/vol-icon && ~/.config/qtile/eww_vol_icon.sh mute &
redshift-gtk -l 35.6612292:139.8649759 &
feh-blur --darken 0 -b 6 &
eww daemon &
nm-applet &
pa-applet --disable-key-grabbing &
# sleep 2
# eww open border &
# eww open border1 &
# eww open border2 &
#blurwal --backend feh -m 1 -b 30 -s 15 &

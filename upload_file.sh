echo $1
echo "Password : ";
read;
Pass=${REPLY}
echo $Pass
file_name="$(basename $1)"
pscp -pw $Pass "$1" "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/WebVideoPlayerDjango/WebVideoPlayer/media/$file_name" 
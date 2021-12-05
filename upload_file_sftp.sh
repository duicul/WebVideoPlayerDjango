echo $1
echo "Password : ";
read;
Pass=${REPLY}
echo $Pass
file_name="$(basename $1)"
sftp "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/WebVideoPlayerDjango/WebVideoPlayer/media/" put "./data.txt"
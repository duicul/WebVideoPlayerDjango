@ECHO OFF
mkdir logs
mkdir database
mkdir json
SET /P PASS="Password: "
::ECHO %PASS%
pscp -i ../Rpi/privatekey.ppk -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/WebVideoPlayerDjango/WebVideoPlayer/logs/*.log*" "logs/"
::pscp -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/*.db" "database/"
::pscp -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/*.json" "json/"
::pscp -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/var/log/auth.log" "logs/auth.log"
::pscp pi@homenetworkdomain.go.ro:/home/pi/error.log logs/error.log
::pscp pi@homenetworkdomain.go.ro:/home/pi/error_monitor.log logs/error_monitor.log
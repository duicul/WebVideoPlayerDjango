@ECHO OFF
echo %1
SET /P PASS="Password: "
::ECHO %PASS%
pscp -pw %PASS% "%1" "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/WebVideoPlayerDjango/WebVideoPlayer/media/%1" 
::pscp -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/*.db" "database/"
::pscp -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/home/pi/*.json" "json/"
::pscp -pw %PASS% "pi@ipnfofuxpslepnbjo.go.ro:/var/log/auth.log" "logs/auth.log"
::pscp pi@homenetworkdomain.go.ro:/home/pi/error.log logs/error.log
::pscp pi@homenetworkdomain.go.ro:/home/pi/error_monitor.log logs/error_monitor.log
@echo off
if "%1" == "" goto usage

 set time_out=300
rem set time_out=60
set infra_base=D:\WWW\server-node\infra

if not exist wget_html.py cd /d %infra_base%\scripts
if not exist wget_html.py goto error1
if exist get_conf.gr%1 goto error2

:loop
echo Start getStatus from GROUP-%1 in %date%_%time% > get_conf.gr%1

rem Get status from ARD in HTML-format
rem
if exist get_conf.srv goto wait
python wget_html.py -i ..\config\gr%1.ini -d ..\status.html\ 

rem Convert HTML-format to JSON-file
rem
if exist get_conf.srv goto wait
if "%2" == "cycle" python html2stat.py -i ..\config\gr%1.ini -d ..\status.html\ -o ..\status\
if NOT "%2" == "cycle" python html2json.py -i ..\config\gr%1.ini -d ..\status.html\ -o ..\status\

rem Check status and autostart registaration
rem
rem if exist get_conf.srv goto wait
rem python start_reg_A1.py -i ..\config\gr%1.ini -d ..\status\

:wait
if NOT "%2" == "cycle" goto stop

rem TIMEOUT /T 300 /NOBREAK
TIMEOUT /T %time_out%

if NOT "%2" == "cycle" goto stop
goto loop

:error1
echo ERROR !!! Not found INFRA scripst (wget_html.py ...) in %infra_base%\scripts !!!
timeout /t 10
exit

:error2
echo ERROR !!! %0 for gorup %1 is runing !!!
timeout /t 10
goto stop

:usage
echo Usage: %0 goup_number [cycle]
echo where	goup_number - number of group (01,02,03)
echo 	cycle - get status of group in cycle

:stop
if exist get_conf.gr%1 del get_conf.gr%1


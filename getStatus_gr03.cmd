@echo off
:loop
if exist get_conf.srv goto wait
python wget_html.py -i config\gr03.ini -d status.html\
if exist get_conf.srv goto wait
python html2json.py -i config\gr03.ini -d status.html\ -o status\
rem if exist get_conf.srv goto wait
rem python start_reg_A1.py -i config\gr03.ini -d status\

:wait
rem TIMEOUT /T 300 /NOBREAK
TIMEOUT /T 60
goto loop
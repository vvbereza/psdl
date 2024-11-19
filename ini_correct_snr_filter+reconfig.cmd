@echo off
rem Stop PSDL
taskkill /f /IM checker2.exe
taskkill /f /IM psdl.exe

rem Configure PSDL
python D:\WWW\server-node\infra\scripts\ini_correct_snr_filter.py -i d:\Work\PSDL\psdl.ini
python D:\WWW\server-node\infra\scripts\ini_reconfig.py -i d:\Work\PSDL\psdl.ini -r d:\Work\PSDL\psdl_runtime.ini
python D:\WWW\server-node\infra\scripts\last_forming.py -d d:\Work\PSDL

rem Start PSDL
cd /d D:\Work
start D:\Work\checker2.exe


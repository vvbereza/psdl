@echo off
rem Stop ASSOC
taskkill /f /IM python.exe

rem Stop PSDL
taskkill /f /IM checker2.exe
taskkill /f /IM psdl.exe

set infra_scripts=D:\WWW\server-node\infra\scripts
cd /d %infra_scripts%

rem Configure PSDL
rem python %infra_scripts%\ini_correct_snr_filter.py -i d:\Work\PSDL\psdl.ini
rem python %infra_scripts%\ini_reconfig.py -i d:\Work\PSDL\psdl.ini -r d:\Work\PSDL\psdl_runtime.ini
rem python %infra_scripts%\ini_reconfig.py -i d:\Work\templates\psdl.ini -r d:\Work\PSDL\psdl.ini

rem Version from Bereza V.V. 2024-11-11
rem
rem python %infra_scripts%\ini_reconfig.py -t d:\Work\PSDL\psdl.ini -p d:\Work\PSDL\psdl_runtime.ini
python %infra_scripts%\ini_reconfig.py -t d:\Work\templates\psdl.ini -p d:\Work\PSDL\psdl.ini

rem Start PSDL
python %infra_scripts%\last_forming.py -d d:\Work\PSDL
cd /d D:\Work
start D:\Work\checker2.exe

rem Start ASSOC
start /MIN /D %infra_scripts%\assoc cmd /c %infra_scripts%\assoc\start_assoc.cmd

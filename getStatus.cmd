@echo off
set infra_base=D:\WWW\server-node\infra
cd /d %infra_base%\scripts

set window=
if "%1" == "cycle" set window=/MIN

 start "Get status I01A" %window% /D %infra_base%\scripts cmd /c getStatus_gr.cmd 01 %1
 start "Get status I02A" %window% /D %infra_base%\scripts cmd /c getStatus_gr.cmd 02 %1
 start "Get status I03A" %window% /D %infra_base%\scripts cmd /c getStatus_gr.cmd 03 %1


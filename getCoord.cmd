@echo off
set sta_ini=%2
set json=%4
set html=../infra/status.html
echo wget_html.py -i %sta_ini% -d %html%
 wget_html.py -i %sta_ini% -d %html%
echo html2json.py -i %sta_ini% -d %html% -o %json%
 html2json-7.py -i %sta_ini% -d %html% -o %json%

echo off
cls
echo downloading file . . .
%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\powershell.exe -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/strawberie-milkshayk/file-visualizer/raw/main/windows/img_generator_V1.exe', 'img_generator_V1.exe')"
echo done!
pause

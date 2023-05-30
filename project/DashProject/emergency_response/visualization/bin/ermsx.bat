REM Add a delay to allow the processes to start
ping 127.0.0.1 -n 3 > nul

REM Stop the Dash app
taskkill /F /IM python.exe /T

REM Stop the Django app
taskkill /F /IM python.exe /T
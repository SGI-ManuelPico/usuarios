@echo off
cd /d "C:\Users\SGI SAS\Documents\GitHub\usuarios"

set START_HOUR=8
set END_HOUR=17

:loop
for /f "tokens=1-3 delims=:." %%a in ("%time%") do (
    set HORA=%%a
    set MIN=%%b
)
set HORA=%HORA: =%

if %HORA% LSS %START_HOUR% goto end
if %HORA% GEQ %END_HOUR% goto end

"C:\Users\SGI SAS\AppData\Local\Programs\Python\Python312\python.exe" main.py

timeout /t 120 /nobreak > nul

goto loop

:end
exit
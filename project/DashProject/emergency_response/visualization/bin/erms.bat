@echo off

REM Start the Dash app batch file in a new command prompt window
@REM call visualizer_env.bat
@REM start cmd /k "visualizer_env.bat"
start /B cmd /C "visualizer_env.bat"

@REM REM Start the Django app batch file in another new command prompt window
@REM start cmd /k "django_runner.bat"
start /B cmd /C "django_runner.bat"
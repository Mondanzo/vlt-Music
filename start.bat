@echo off
title Music Bot
echo Starting Bot
python --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO nopython
python "main.py"

:nopython
echo ERROR - Python is missing!
:end
pause
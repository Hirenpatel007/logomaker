@echo off
echo AI LogoMaker by Hiren Patel
echo Starting Django Development Server...
echo.

cd /d "%~dp0"
py manage.py runserver 8000

pause
@echo off
echo AI LogoMaker Setup by Hiren Patel
echo Installing dependencies and setting up the project...
echo.

cd /d "%~dp0"

echo Installing basic requirements...
pip install -r requirements_basic.txt

echo Making migrations...
py manage.py makemigrations

echo Applying migrations...
py manage.py migrate

echo Creating superuser (admin/admin123)...
echo from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@logomaker.com', 'admin123') | py manage.py shell

echo.
echo Setup complete! Run 'run_server.bat' to start the server.
echo Admin login: admin / admin123
echo.
pause
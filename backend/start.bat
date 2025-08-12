@echo off
cd /d %~dp0
echo Starting Flask backend server...
set FLASK_APP=app.py
set FLASK_ENV=development
python -m flask run --port=5000
pause

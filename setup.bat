@echo off

set "python_path=%LOCALAPPDATA%\Microsoft\WindowsApps\python3.7.exe"

if exist "%python_path%" (
	if exist "venv" (
		echo Virtual environment found
	) else (
	echo Creating virtual environment...
		python3.7 -m venv venv
		echo Virtual environment created
	)
	call venv\Scripts\activate
	echo installing packages...
	pip install fastapi pygame pyserial uvicorn pytz inputs
	MOVE .\control\Start.py .\Start.py
	MOVE .\control\Start.bat .\Start.bat
	echo Finished!
) else (
    echo Python 3.7 is not installed. Please install it via the Microsoft Store.
)
pause
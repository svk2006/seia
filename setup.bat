@echo off
REM Quick start script for Windows

echo.
echo ========================================
echo   Crop Stress Advisory - Quick Start
echo ========================================
echo.

REM Backend setup
echo [1/4] Setting up backend...
cd backend

if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -q -r requirements.txt

echo Training ML model...
python -c "from models import CropStressModel; m = CropStressModel(); m.train('training_data.csv')"

echo.
echo ========================================
echo Backend setup complete!
echo Navigate to backend folder and run:
echo   venv\Scripts\activate.bat
echo   python app.py
echo ========================================
echo.

REM Frontend setup
echo [2/4] Setting up frontend...
cd ..\frontend

if not exist node_modules (
    echo Installing Node dependencies (this may take a minute)...
    call npm install -q
)

echo.
echo ========================================
echo Frontend setup complete!
echo Navigate to frontend folder and run:
echo   npm start
echo ========================================
echo.

echo.
echo ========================================
echo SETUP COMPLETE! Next steps:
echo ========================================
echo.
echo 1. Open TWO terminal windows
echo.
echo Terminal 1 - Start Backend:
echo   cd backend
echo   venv\Scripts\activate.bat
echo   python app.py
echo.
echo Terminal 2 - Start Frontend:
echo   cd frontend
echo   npm start
echo.
echo Then visit http://localhost:3000 in your browser
echo.
echo ========================================
echo.

pause

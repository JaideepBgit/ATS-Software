@echo off
echo Installing Backend Dependencies...
cd backend
C:/Users/jaide/anaconda3/Scripts/activate
conda activate py310
pip install -r requirements.txt
echo.
echo Backend dependencies installed!
pause

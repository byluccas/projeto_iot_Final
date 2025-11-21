@echo off
echo ====================================
echo    INICIANDO SISTEMA IoT
echo ====================================
echo.
cd /d "C:\xampp\htdocs\MicroPython\projeto_iot"
echo Instalando dependências...
pip install flask
echo.
echo Iniciando servidor...
python app.py
echo.
pause
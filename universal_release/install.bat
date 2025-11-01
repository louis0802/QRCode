@echo off
chcp 65001 >nul
echo ==========================================
echo QRCode Converter - Windows 安裝
echo ==========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 Python
    echo.
    echo 請先安裝 Python 3.8+: https://www.python.org/downloads/
    echo 安裝時勾選 "Add Python to PATH"
    pause
    exit /b 1
)

echo 找到 Python:
python --version
echo.
echo 正在安裝套件...
pip install -r requirements.txt

echo.
echo ==========================================
echo ✅ 安裝完成！
echo ==========================================
pause

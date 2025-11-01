@echo off
chcp 65001 >nul
echo QR Code 轉換程式
echo ==========================================
echo.

REM 檢查 Python 是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 Python，請先安裝 Python 3.8 或更新版本
    echo 下載: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 檢查套件是否安裝
python -c "import cv2, qrcode, pyzbar" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安裝必要套件...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [錯誤] 套件安裝失敗
        pause
        exit /b 1
    )
)

REM 執行程式
echo.
echo 開始處理 QR code...
echo ==========================================
echo.
python qrcode_converter.py

echo.
echo ==========================================
echo 按任意鍵關閉視窗...
pause >nul

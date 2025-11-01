@echo off
chcp 65001 >nul
echo ==========================================
echo QRCode Converter
echo ==========================================
echo.

if not exist "input\*.*" (
    echo [提示] input 資料夾是空的
    echo 請放入 QR code 圖片後再執行
    pause
    exit /b 0
)

python qrcode_converter.py

echo.
echo 按任意鍵關閉...
pause >nul

#!/bin/bash
echo "=========================================="
echo "QRCode Converter"
echo "=========================================="
echo ""

if [ ! "$(ls -A input)" ]; then
    echo "[提示] input 資料夾是空的"
    echo "請放入 QR code 圖片後再執行"
    exit 0
fi

python3 qrcode_converter.py

echo ""
echo "完成！按 Enter 關閉..."
read

#!/bin/bash
echo "=========================================="
echo "QRCode Converter - 安裝"
echo "=========================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[錯誤] 找不到 Python 3"
    echo "請先安裝 Python 3.8+"
    exit 1
fi

echo "找到 Python:"
python3 --version
echo ""
echo "正在安裝套件..."
pip3 install -r requirements.txt

echo ""
echo "=========================================="
echo "✅ 安裝完成！"
echo "=========================================="

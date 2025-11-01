#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
建立測試用的 QR code 圖片
"""

import qrcode
from PIL import Image
from pathlib import Path


def create_single_qrcode(content: str, filename: str):
    """建立單個 QR code"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    output_path = Path("input") / filename
    img.save(str(output_path))
    print(f"✅ 已建立: {filename} - 內容: {content}")


def create_multiple_qrcodes_image(contents: list[str], filename: str):
    """建立包含多個 QR code 的圖片"""
    # 為每個內容建立 QR code
    qr_images = []
    for content in contents:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=2,
        )
        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_images.append(img)
    
    # 計算組合圖片的大小
    qr_width = qr_images[0].size[0]
    qr_height = qr_images[0].size[1]
    
    # 水平排列所有 QR code，中間加上間距
    spacing = 20
    total_width = qr_width * len(qr_images) + spacing * (len(qr_images) - 1)
    total_height = qr_height
    
    # 建立白色背景
    combined = Image.new('RGB', (total_width, total_height), 'white')
    
    # 貼上每個 QR code
    x_offset = 0
    for img in qr_images:
        combined.paste(img, (x_offset, 0))
        x_offset += qr_width + spacing
    
    # 儲存
    output_path = Path("input") / filename
    combined.save(str(output_path))
    print(f"✅ 已建立: {filename} - 包含 {len(contents)} 個 QR code")
    for i, content in enumerate(contents, 1):
        print(f"   QR code #{i}: {content}")


def main():
    """主程式"""
    print("建立測試用的 QR code 圖片")
    print("=" * 60)
    
    # 確保 input 資料夾存在
    Path("input").mkdir(exist_ok=True)
    
    # 測試案例 1: 單個 QR code
    print("\n📝 測試案例 1: 單個 QR code")
    create_single_qrcode(
        "[CVS]|MAVVLQ041597|5HVW486G4LV8",
        "test_single.png"
    )
    
    # 測試案例 2: 包含 2 個 QR code 的圖片
    print("\n📝 測試案例 2: 包含 2 個 QR code")
    create_multiple_qrcodes_image(
        [
            "[CVS]|TEST123456|ABCD1234",
            "[CVS]|SAMPLE789|XYZ9876"
        ],
        "test_double.png"
    )
    
    # 測試案例 3: 包含 3 個 QR code 的圖片
    print("\n📝 測試案例 3: 包含 3 個 QR code")
    create_multiple_qrcodes_image(
        [
            "[CVS]|CARD001|AAA111",
            "[CVS]|CARD002|BBB222",
            "[CVS]|CARD003|CCC333"
        ],
        "test_triple.png"
    )
    
    # 測試案例 4: 不含 [CVS] 的 QR code（測試警告訊息）
    print("\n📝 測試案例 4: 不含 [CVS] 的 QR code")
    create_single_qrcode(
        "[MyCard]|ALREADY|CONVERTED",
        "test_no_cvs.png"
    )
    
    print("\n" + "=" * 60)
    print("✅ 測試圖片建立完成！")
    print("請執行 'python3 qrcode_converter.py' 來測試轉換功能")


if __name__ == "__main__":
    main()

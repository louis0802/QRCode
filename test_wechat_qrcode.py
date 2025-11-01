#!/usr/bin/env python3
"""測試 WeChat QRCode 偵測器"""
import cv2
import os
from PIL import Image
import numpy as np

print("=" * 60)
print("測試 WeChat QRCode 偵測器")
print("=" * 60)

# 檢查模型檔案
model_dir = 'models'
model_files = ['detect.prototxt', 'detect.caffemodel', 'sr.prototxt', 'sr.caffemodel']

print("\n1. 檢查模型檔案...")
for filename in model_files:
    filepath = os.path.join(model_dir, filename)
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"   ✓ {filename}: {size:,} bytes")
    else:
        print(f"   ✗ {filename}: 檔案不存在")

# 嘗試初始化 WeChat QRCode
print("\n2. 初始化 WeChat QRCode 偵測器...")
try:
    detector = cv2.wechat_qrcode_WeChatQRCode(
        os.path.join(model_dir, 'detect.prototxt'),
        os.path.join(model_dir, 'detect.caffemodel'),
        os.path.join(model_dir, 'sr.prototxt'),
        os.path.join(model_dir, 'sr.caffemodel')
    )
    print("   ✓ WeChat QRCode 初始化成功！")
    
    # 測試偵測功能
    print("\n3. 測試 QR code 偵測...")
    test_image = os.path.join('input', 'S__430292998.jpg')
    
    if os.path.exists(test_image):
        # 讀取圖片
        image = Image.open(test_image)
        img_array = np.array(image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # 偵測 QR code
        results, points = detector.detectAndDecode(img_bgr)
        
        print(f"   偵測到 {len(results)} 個 QR code")
        for idx, data in enumerate(results, 1):
            if data:
                print(f"   QR Code #{idx}: {data[:50]}..." if len(data) > 50 else f"   QR Code #{idx}: {data}")
        
        if len(results) > 0:
            print("\n   ✓ WeChat QRCode 偵測功能正常！")
        else:
            print("\n   ⚠ 未偵測到 QR code（可能是測試圖片問題）")
    else:
        print(f"   ⚠ 測試圖片不存在: {test_image}")
        
except AttributeError:
    print("   ✗ cv2 模組沒有 wechat_qrcode_WeChatQRCode 屬性")
    print("   請確認已安裝 opencv-contrib-python-headless")
except Exception as e:
    print(f"   ✗ 初始化失敗: {e}")

print("\n" + "=" * 60)
print("測試完成")
print("=" * 60)

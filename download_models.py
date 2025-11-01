#!/usr/bin/env python3
"""下載 WeChat QRCode 模型檔案"""
import urllib.request
import os

# 模型檔案的正確 URL
model_urls = {
    'detect.prototxt': 'https://github.com/opencv/opencv_3rdparty/raw/wechat_qrcode_20210119/detect.prototxt',
    'detect.caffemodel': 'https://github.com/opencv/opencv_3rdparty/raw/wechat_qrcode_20210119/detect.caffemodel',
    'sr.prototxt': 'https://github.com/opencv/opencv_3rdparty/raw/wechat_qrcode_20210119/sr.prototxt',
    'sr.caffemodel': 'https://github.com/opencv/opencv_3rdparty/raw/wechat_qrcode_20210119/sr.caffemodel'
}

models_dir = 'models'
os.makedirs(models_dir, exist_ok=True)

print("開始下載 WeChat QRCode 模型檔案...")

for filename, url in model_urls.items():
    filepath = os.path.join(models_dir, filename)
    print(f"\n下載 {filename}...")
    print(f"URL: {url}")
    
    try:
        urllib.request.urlretrieve(url, filepath)
        file_size = os.path.getsize(filepath)
        print(f"✓ 成功！檔案大小: {file_size:,} bytes")
    except Exception as e:
        print(f"✗ 失敗: {e}")

print("\n下載完成！")
print("\n檔案清單:")
for filename in model_urls.keys():
    filepath = os.path.join(models_dir, filename)
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  {filename}: {size:,} bytes")

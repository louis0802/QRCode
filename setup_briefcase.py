#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Briefcase 建立跨平台版本
支援 Windows (x64/ARM), macOS, Linux
"""

import subprocess
import sys
from pathlib import Path


def install_briefcase():
    """安裝 Briefcase"""
    print("安裝 Briefcase...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "briefcase"], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Briefcase 安裝成功")
        return True
    else:
        print("❌ Briefcase 安裝失敗")
        print(result.stderr)
        return False


def create_pyproject_toml():
    """建立 pyproject.toml 設定檔"""
    config = """[tool.briefcase]
project_name = "QRCode Converter"
bundle = "com.mycard"
version = "1.0.0"
url = "https://github.com/yourusername/qrcode-converter"
license = "MIT license"
author = "Your Name"
author_email = "your.email@example.com"

[tool.briefcase.app.qrcodeconverter]
formal_name = "QRCode Converter"
description = "轉換 QR code 從 [CVS] 到 [MyCard]"
long_description = \"\"\"QR Code 轉換程式
將 QR code 中的 [CVS] 轉換為 [MyCard]
支援批次處理多個圖片
\"\"\"
icon = "icon"  # 會自動尋找 icon.png
sources = ["qrcode_converter"]
test_sources = []

requires = [
    "opencv-python>=4.8.0",
    "qrcode[pil]>=7.4.2",
    "Pillow>=10.0.0",
    "pyzbar>=0.1.9",
]

test_requires = []

[tool.briefcase.app.qrcodeconverter.macOS]
requires = []

[tool.briefcase.app.qrcodeconverter.linux]
requires = []
system_requires = []

[tool.briefcase.app.qrcodeconverter.windows]
requires = []
system_requires = []

[tool.briefcase.app.qrcodeconverter.iOS]
requires = []

[tool.briefcase.app.qrcodeconverter.android]
requires = []
"""
    
    with open('pyproject.toml', 'w', encoding='utf-8') as f:
        f.write(config)
    
    print("✅ 已建立 pyproject.toml")


def prepare_briefcase_structure():
    """準備 Briefcase 專案結構"""
    print("\n準備專案結構...")
    
    # 建立套件資料夾
    app_folder = Path('qrcodeconverter')
    if not app_folder.exists():
        app_folder.mkdir()
    
    # 複製主程式並重新命名為 __main__.py
    import shutil
    shutil.copy('qrcode_converter.py', app_folder / '__main__.py')
    
    # 建立 __init__.py
    (app_folder / '__init__.py').write_text('"""QRCode Converter Application"""\n')
    
    print("✅ 專案結構已準備完成")


def main():
    """主程式"""
    print("=" * 60)
    print("QRCode Converter - Briefcase 跨平台打包")
    print("=" * 60)
    print("\n這個工具會使用 Briefcase 建立真正的跨平台應用程式")
    print("可以在 Windows (x64/ARM), macOS, Linux 上執行\n")
    
    # 步驟 1: 安裝 Briefcase
    print("步驟 1: 安裝 Briefcase")
    if not install_briefcase():
        return
    
    # 步驟 2: 建立設定檔
    print("\n步驟 2: 建立設定檔")
    create_pyproject_toml()
    
    # 步驟 3: 準備專案結構
    print("\n步驟 3: 準備專案結構")
    prepare_briefcase_structure()
    
    # 步驟 4: 說明後續步驟
    print("\n" + "=" * 60)
    print("✅ 準備完成！")
    print("=" * 60)
    print("\n接下來的步驟：")
    print("\n【在當前系統（macOS）建立應用程式】")
    print("  briefcase create")
    print("  briefcase build")
    print("  briefcase package")
    print("\n【在 Windows 上建立 Windows 版本】")
    print("  1. 將專案複製到 Windows 電腦")
    print("  2. 安裝 Python 和 Briefcase")
    print("  3. 執行相同的命令")
    print("\n【支援的平台】")
    print("  • Windows (x64/ARM)")
    print("  • macOS (Intel/Apple Silicon)")
    print("  • Linux")
    print("\n💡 Briefcase 會自動處理所有依賴和打包細節！")


if __name__ == "__main__":
    main()

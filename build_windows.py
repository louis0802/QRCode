#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 打包腳本
使用 PyInstaller 將程式打包成 Windows 可執行檔
"""

import os
import shutil
import subprocess
from pathlib import Path


def clean_build_folders():
    """清理之前的建置資料夾"""
    folders_to_clean = ['build', 'dist', '__pycache__']
    for folder in folders_to_clean:
        if Path(folder).exists():
            shutil.rmtree(folder)
            print(f"✓ 已清理: {folder}/")
    
    # 清理 .spec 檔案
    spec_files = list(Path('.').glob('*.spec'))
    for spec_file in spec_files:
        spec_file.unlink()
        print(f"✓ 已刪除: {spec_file}")


def build_executable():
    """使用 PyInstaller 建立可執行檔"""
    print("\n開始建立 Windows 可執行檔...")
    print("=" * 60)
    
    # PyInstaller 命令
    cmd = [
        'pyinstaller',
        '--onefile',                    # 打包成單一檔案
        '--name=QRCodeConverter',       # 執行檔名稱
        '--console',                    # 顯示控制台視窗
        '--add-data=README.md:.',       # 包含 README
        '--hidden-import=pyzbar',       # 確保包含 pyzbar
        '--hidden-import=cv2',          # 確保包含 opencv
        '--hidden-import=qrcode',       # 確保包含 qrcode
        '--hidden-import=PIL',          # 確保包含 Pillow
        'qrcode_converter.py'
    ]
    
    # 執行打包
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✅ 建置成功！")
        return True
    else:
        print("\n❌ 建置失敗！")
        print(result.stderr)
        return False


def create_release_package():
    """建立發布套件"""
    print("\n建立發布套件...")
    print("=" * 60)
    
    # 建立發布資料夾
    release_folder = Path('release')
    if release_folder.exists():
        shutil.rmtree(release_folder)
    release_folder.mkdir()
    
    # 複製可執行檔（在 macOS 上是無副檔名的，在 Windows 上是 .exe）
    exe_file_with_ext = Path('dist/QRCodeConverter.exe')
    exe_file_no_ext = Path('dist/QRCodeConverter')
    
    if exe_file_with_ext.exists():
        shutil.copy(exe_file_with_ext, release_folder / 'QRCodeConverter.exe')
        print(f"✓ 已複製: QRCodeConverter.exe")
    elif exe_file_no_ext.exists():
        # 在 macOS 上測試建置，複製為 macOS 版本
        shutil.copy(exe_file_no_ext, release_folder / 'QRCodeConverter')
        print(f"✓ 已複製: QRCodeConverter (macOS 版本)")
        print(f"⚠️  注意: 在 Windows 電腦上重新執行此腳本以建立 .exe 檔案")
    else:
        print(f"❌ 找不到可執行檔")
        return False
    
    # 建立 input 和 output 資料夾
    (release_folder / 'input').mkdir()
    (release_folder / 'output').mkdir()
    print("✓ 已建立: input/ 和 output/ 資料夾")
    
    # 複製程式碼檔案（作為備份）
    shutil.copy('qrcode_converter.py', release_folder / 'qrcode_converter.py')
    print("✓ 已複製: qrcode_converter.py")
    
    # 複製 requirements.txt
    shutil.copy('requirements.txt', release_folder / 'requirements.txt')
    print("✓ 已複製: requirements.txt")
    
    # 複製說明檔案
    if Path('README.md').exists():
        shutil.copy('README.md', release_folder / 'README.md')
        print("✓ 已複製: README.md")
    
    # 建立 Windows 使用說明
    create_windows_readme(release_folder)
    
    # 建立 run.bat 批次檔
    create_batch_file(release_folder)
    
    print(f"\n✅ 發布套件已建立在: {release_folder.absolute()}")
    return True


def create_windows_readme(release_folder):
    """建立 Windows 使用說明"""
    readme_content = """# QR Code 轉換程式 - Windows 版本

## 快速開始

### 方法 1: 使用可執行檔（推薦）
1. 將要轉換的 QR code 圖片放入 `input` 資料夾
2. 雙擊 `QRCodeConverter.exe` 執行程式
3. 查看 `output` 資料夾中的轉換結果

### 方法 2: 使用 Python 腳本
如果可執行檔無法運作，可以直接使用 Python：

1. 安裝 Python 3.8 或更新版本
2. 開啟命令提示字元（CMD）
3. 執行: `pip install -r requirements.txt`
4. 執行: `python qrcode_converter.py`
5. 或直接雙擊 `run.bat`

## 功能說明

- ✅ 自動偵測圖片中的多個 QR code
- ✅ 將 [CVS] 轉換為 [MyCard]
- ✅ 支援多種圖片格式：PNG, JPG, JPEG, BMP, GIF, TIFF
- ✅ 自動清空 output 資料夾
- ✅ 生成偵測不完整報告 (incomplete_files_report.txt)

## 系統需求

### 使用可執行檔
- Windows 10 或更新版本
- Visual C++ Redistributable (如執行時出錯請安裝)
  https://aka.ms/vs/17/release/vc_redist.x64.exe

### 使用 Python 腳本
- Python 3.8+
- pip (Python 套件管理器)

## 重要：zbar 函式庫

程式使用 pyzbar 來偵測 QR code，在 Windows 上需要額外安裝：

**選項 1: 使用 conda (推薦)**
```
conda install -c conda-forge zbar
```

**選項 2: 手動安裝 DLL**
1. 下載 zbar: http://zbar.sourceforge.net/download.html
2. 將 `libzbar-64.dll` 放在程式目錄中

**選項 3: 使用 OpenCV (無需額外安裝)**
程式會自動偵測，如果沒有 zbar 則使用 OpenCV（準確度略低）

## 輸出說明

### QR code 檔案
- 單個 QR code: 保留原檔名
- 多個 QR code: 檔名_1.jpg, 檔名_2.jpg, 檔名_3.jpg

### 報告檔案
- `incomplete_files_report.txt`: 列出偵測數量不足 3 個的檔案

## 常見問題

### Q: 執行時出現「找不到 DLL」錯誤？
A: 安裝 Visual C++ Redistributable

### Q: 無法偵測到 QR code？
A: 
1. 安裝 zbar 函式庫（見上方說明）
2. 確認圖片品質良好
3. 檢查 QR code 是否清晰

### Q: 程式執行完立即關閉？
A: 使用 run.bat 或在 CMD 中執行，可看到輸出訊息

## 技術支援

詳細文件請參考 README.md

---
版本: 1.0
"""
    
    readme_path = release_folder / 'Windows使用說明.txt'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✓ 已建立: Windows使用說明.txt")


def create_batch_file(release_folder):
    """建立 Windows 批次檔"""
    batch_content = """@echo off
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
"""
    
    batch_path = release_folder / 'run.bat'
    with open(batch_path, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print("✓ 已建立: run.bat")



def main():
    """主程式"""
    print("QR Code 轉換程式 - Windows 打包工具")
    print("=" * 60)
    
    # 清理舊的建置檔案
    print("\n步驟 1: 清理舊的建置檔案")
    clean_build_folders()
    
    # 建立可執行檔
    print("\n步驟 2: 建立可執行檔")
    if not build_executable():
        print("\n❌ 建置失敗，請檢查錯誤訊息")
        return
    
    # 建立發布套件
    print("\n步驟 3: 建立發布套件")
    if not create_release_package():
        print("\n❌ 建立發布套件失敗")
        return
    
    print("\n" + "=" * 60)
    print("✅ 所有步驟完成！")
    print("\n📦 發布檔案位置：release/")
    print("\n下一步：")
    print("1. 將 release 資料夾複製到 Windows 電腦")
    print("2. 閱讀 Windows使用說明.txt")
    print("3. 執行 QRCodeConverter.exe")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
建立 Windows 可攜版本（不需要打包成 .exe）
適用於 Windows ARM 和所有 Windows 系統
"""

import shutil
from pathlib import Path


def create_portable_package():
    """建立 Windows 可攜版本"""
    print("建立 Windows 可攜版本")
    print("=" * 60)
    
    # 建立發布資料夾
    release_folder = Path('windows_portable')
    if release_folder.exists():
        shutil.rmtree(release_folder)
    release_folder.mkdir()
    
    print("✓ 建立資料夾: windows_portable/")
    
    # 複製主程式
    shutil.copy('qrcode_converter.py', release_folder / 'qrcode_converter.py')
    print("✓ 已複製: qrcode_converter.py")
    
    # 複製 requirements.txt
    shutil.copy('requirements.txt', release_folder / 'requirements.txt')
    print("✓ 已複製: requirements.txt")
    
    # 建立 input 和 output 資料夾
    (release_folder / 'input').mkdir()
    (release_folder / 'output').mkdir()
    print("✓ 已建立: input/ 和 output/ 資料夾")
    
    # 建立 Windows 批次檔
    create_run_bat(release_folder)
    
    # 建立安裝腳本
    create_install_bat(release_folder)
    
    # 建立使用說明
    create_readme(release_folder)
    
    print(f"\n✅ Windows 可攜版本已建立在: {release_folder.absolute()}")
    print("\n📦 包含檔案：")
    print("   • qrcode_converter.py - 主程式")
    print("   • install.bat - 安裝套件（第一次使用時執行）")
    print("   • run.bat - 執行程式")
    print("   • requirements.txt - 套件清單")
    print("   • 使用說明.txt - 詳細說明")
    print("   • input/ - 放置 QR code 圖片")
    print("   • output/ - 輸出資料夾")


def create_install_bat(release_folder):
    """建立安裝批次檔"""
    batch_content = """@echo off
chcp 65001 >nul
echo ==========================================
echo QR Code 轉換程式 - 套件安裝
echo ==========================================
echo.

REM 檢查 Python 是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 Python
    echo.
    echo 請先安裝 Python 3.8 或更新版本：
    echo https://www.python.org/downloads/
    echo.
    echo 安裝時請勾選 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [提示] 找到 Python:
python --version
echo.

REM 升級 pip
echo [1/3] 升級 pip...
python -m pip install --upgrade pip

REM 安裝基本套件
echo.
echo [2/3] 安裝基本套件...
pip install opencv-python qrcode[pil] Pillow

REM 嘗試安裝 pyzbar
echo.
echo [3/3] 嘗試安裝 pyzbar...
pip install pyzbar
if errorlevel 1 (
    echo.
    echo [提示] pyzbar 安裝失敗（這是正常的）
    echo 程式將使用 OpenCV 作為備用偵測器
    echo 如需更好的偵測效果，請參考"使用說明.txt"安裝 zbar
)

echo.
echo ==========================================
echo ✅ 安裝完成！
echo ==========================================
echo.
echo 下一步：
echo 1. 將 QR code 圖片放入 input 資料夾
echo 2. 雙擊 run.bat 執行程式
echo.
pause
"""
    
    batch_path = release_folder / 'install.bat'
    with open(batch_path, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print("✓ 已建立: install.bat")


def create_run_bat(release_folder):
    """建立執行批次檔"""
    batch_content = """@echo off
chcp 65001 >nul
echo ==========================================
echo QR Code 轉換程式
echo ==========================================
echo.

REM 檢查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 Python
    echo 請先執行 install.bat 安裝
    pause
    exit /b 1
)

REM 檢查 input 資料夾是否有檔案
if not exist "input\\*.*" (
    echo [提示] input 資料夾是空的
    echo 請先將 QR code 圖片放入 input 資料夾
    echo.
    pause
    exit /b 0
)

REM 執行程式
echo 開始處理 QR code...
echo.
python qrcode_converter.py

REM 檢查是否有報告
if exist "incomplete_files_report.txt" (
    echo.
    echo ⚠️  發現不完整檔案報告
    echo 請查看 incomplete_files_report.txt
)

echo.
echo ==========================================
echo 按任意鍵關閉視窗...
pause >nul
"""
    
    batch_path = release_folder / 'run.bat'
    with open(batch_path, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print("✓ 已建立: run.bat")


def create_readme(release_folder):
    """建立使用說明"""
    readme_content = """# QR Code 轉換程式 - Windows 可攜版本

## ✨ 特點

- ✅ 支援所有 Windows 系統（包括 Windows ARM）
- ✅ 不需要打包，直接使用 Python 腳本
- ✅ 可攜式設計，複製即用
- ✅ 自動偵測多個 QR code
- ✅ 自動清空輸出資料夾

## 🚀 快速開始（三步驟）

### 第一次使用

1. **安裝 Python**
   - 下載：https://www.python.org/downloads/
   - 執行安裝程式
   - ⚠️ 重要：勾選「Add Python to PATH」
   - 完成後重新開機

2. **安裝套件**
   - 雙擊 `install.bat`
   - 等待安裝完成
   - 如果看到 pyzbar 安裝失敗的訊息，這是正常的

3. **開始使用**
   - 將 QR code 圖片放入 `input` 資料夾
   - 雙擊 `run.bat` 執行程式
   - 查看 `output` 資料夾中的結果

### 之後使用

每次使用只需要：
1. 放入圖片到 `input` 資料夾
2. 雙擊 `run.bat`
3. 查看 `output` 資料夾

## 📁 檔案說明

```
windows_portable/
├── install.bat          # 第一次使用時執行（安裝套件）
├── run.bat              # 執行程式（每次使用）
├── qrcode_converter.py  # 主程式
├── requirements.txt     # 套件清單
├── 使用說明.txt         # 本檔案
├── input/               # 放置原始 QR code 圖片
└── output/              # 轉換後的輸出位置
```

## 🔧 進階設定：安裝 zbar（可選）

為了獲得更好的 QR code 偵測效果，可以安裝 zbar：

### 方法 1：使用 Conda（推薦）
```bash
conda install -c conda-forge zbar
```

### 方法 2：手動安裝（Windows x64）
1. 下載 zbar：http://zbar.sourceforge.net/download.html
2. 解壓縮找到 `libzbar-64.dll`
3. 將 DLL 複製到程式目錄

### 方法 3：不安裝
程式會自動使用 OpenCV 偵測器（準確度略低但足夠使用）

## ⚠️ Windows ARM 特別說明

如果你使用的是 Windows ARM（如 Surface Pro X）：

1. **Python 安裝**
   - 選擇 ARM64 版本的 Python
   - 或使用 x64 版本（會透過模擬執行）

2. **套件安裝**
   - 所有套件都支援 ARM
   - opencv-python 和 qrcode 可以正常使用

3. **zbar 支援**
   - Windows ARM 上 pyzbar 可能無法使用
   - 這沒關係，程式會自動使用 OpenCV
   - OpenCV 在 ARM 上運作良好

## 💡 使用技巧

### 批次處理
- 可以一次放入多張圖片
- 程式會自動處理所有圖片
- 每張圖片可包含多個 QR code

### 檢查結果
- 查看 `incomplete_files_report.txt`
- 列出沒有偵測到 3 個 QR code 的檔案

### 重複執行
- output 資料夾會自動清空
- 不需要手動刪除舊檔案

## 🐛 疑難排解

### 問題 1：找不到 Python
**原因**：Python 未安裝或未加入 PATH
**解決**：
1. 重新安裝 Python
2. 勾選「Add Python to PATH」
3. 重新開機

### 問題 2：套件安裝失敗
**原因**：網路問題或權限不足
**解決**：
```bash
# 使用管理員權限執行 CMD，然後：
pip install --user -r requirements.txt
```

### 問題 3：無法偵測 QR code
**原因**：圖片品質或 zbar 未安裝
**解決**：
1. 檢查圖片是否清晰
2. 嘗試安裝 zbar（見上方說明）
3. 即使沒有 zbar，OpenCV 也能偵測大部分 QR code

### 問題 4：程式執行後立即關閉
**原因**：Python 環境問題
**解決**：
1. 在 CMD 中手動執行：`python qrcode_converter.py`
2. 查看完整的錯誤訊息
3. 確認所有套件已安裝

### 問題 5：Windows 防毒軟體警告
**原因**：批次檔可能被誤判
**解決**：
1. 將資料夾加入防毒軟體的白名單
2. 或直接在 CMD 執行：`python qrcode_converter.py`

## 📞 系統需求

- **作業系統**：Windows 10/11（包括 ARM 版本）
- **Python**：3.8 或更新版本
- **磁碟空間**：約 500MB（包含 Python 和套件）
- **記憶體**：建議 4GB 以上

## 📝 功能說明

### 轉換功能
- 自動將 `[CVS]` 替換為 `[MyCard]`
- 保留其他內容不變

### 檔案命名
- 單個 QR code：保留原檔名
- 多個 QR code：
  - 原檔名_1.jpg
  - 原檔名_2.jpg
  - 原檔名_3.jpg

### 支援格式
- PNG (.png)
- JPEG (.jpg, .jpeg)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff)

## 🎯 效能說明

- 每張圖片處理時間：1-5 秒
- 視圖片大小和 QR code 數量而定
- Windows ARM 上速度略慢於 x64（如使用模擬）

---

版本：1.0
最後更新：2025-11-01
適用平台：Windows 10/11 (x64, ARM64)

如有問題，請確認已正確安裝 Python 和相關套件。
"""
    
    readme_path = release_folder / '使用說明.txt'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✓ 已建立: 使用說明.txt")


def main():
    """主程式"""
    print("\n" + "=" * 60)
    print("QR Code 轉換程式 - Windows 可攜版本建立工具")
    print("適用於所有 Windows 系統（包括 Windows ARM）")
    print("=" * 60 + "\n")
    
    create_portable_package()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    print("\n📦 下一步：")
    print("1. 將 windows_portable 資料夾複製到 Windows 電腦")
    print("2. 在 Windows 上雙擊 install.bat 安裝套件")
    print("3. 之後每次使用只需雙擊 run.bat")
    print("\n💡 提示：這個版本適用於所有 Windows 系統，包括 ARM！")


if __name__ == "__main__":
    main()

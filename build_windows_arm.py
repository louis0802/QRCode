#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
建立 Windows (包括 ARM) 可用的發布包
不依賴 PyInstaller，直接使用 Python 腳本
"""

import shutil
from pathlib import Path


def create_windows_arm_package():
    """建立 Windows ARM 相容的發布包"""
    print("建立 Windows ARM 相容發布包")
    print("=" * 60)
    
    # 建立發布資料夾
    release_folder = Path('release-windows-arm')
    if release_folder.exists():
        shutil.rmtree(release_folder)
    release_folder.mkdir()
    
    print("✓ 已建立 release-windows-arm 資料夾")
    
    # 複製程式檔案
    shutil.copy('qrcode_converter.py', release_folder / 'qrcode_converter.py')
    print("✓ 已複製: qrcode_converter.py")
    
    # 複製 requirements.txt（移除 pyinstaller）
    with open('requirements.txt', 'r') as f:
        requirements = [line for line in f if 'pyinstaller' not in line.lower()]
    
    with open(release_folder / 'requirements.txt', 'w') as f:
        f.writelines(requirements)
    print("✓ 已建立: requirements.txt")
    
    # 複製 README
    if Path('README.md').exists():
        shutil.copy('README.md', release_folder / 'README.md')
        print("✓ 已複製: README.md")
    
    # 建立資料夾
    (release_folder / 'input').mkdir()
    (release_folder / 'output').mkdir()
    print("✓ 已建立: input/ 和 output/ 資料夾")
    
    # 建立 Windows ARM 專用的使用說明
    create_windows_arm_readme(release_folder)
    
    # 建立啟動批次檔
    create_run_bat(release_folder)
    
    # 建立安裝腳本
    create_install_bat(release_folder)
    
    print("\n" + "=" * 60)
    print(f"✅ Windows ARM 發布包已建立！")
    print(f"📦 位置: {release_folder.absolute()}")
    print("\n📝 使用說明：")
    print("1. 將 release-windows-arm 資料夾複製到 Windows ARM 電腦")
    print("2. 雙擊 install.bat 安裝所需套件")
    print("3. 雙擊 run.bat 執行程式")


def create_windows_arm_readme(release_folder):
    """建立 Windows ARM 使用說明"""
    content = """# QR Code 轉換程式 - Windows ARM 版本

## 🎯 適用系統

- Windows 11 ARM64
- Surface Pro X
- 其他 ARM 架構的 Windows 電腦

## 🚀 快速開始（3 步驟）

### 步驟 1: 安裝 Python

1. 下載 Python for Windows ARM64
   - 官網: https://www.python.org/downloads/windows/
   - 選擇 "ARM64 installer"
   - **重要**: 安裝時勾選「Add Python to PATH」

2. 確認安裝成功
   ```
   按 Win+R，輸入 cmd，按 Enter
   輸入: python --version
   應該會顯示 Python 3.x.x
   ```

### 步驟 2: 安裝所需套件

**方法 A: 自動安裝（推薦）**
- 雙擊 `install.bat`
- 等待安裝完成

**方法 B: 手動安裝**
```bash
pip install -r requirements.txt
```

### 步驟 3: 使用程式

1. 將 QR code 圖片放入 `input` 資料夾
2. 雙擊 `run.bat` 執行程式
3. 查看 `output` 資料夾中的轉換結果

## 📋 功能說明

✅ 自動偵測圖片中的多個 QR code（一張圖最多 3 個）
✅ 將 [CVS] 轉換為 [MyCard]
✅ 支援格式：PNG, JPG, JPEG, BMP, GIF, TIFF
✅ 自動清空 output 資料夾
✅ 生成偵測報告 (incomplete_files_report.txt)

## ⚠️ 重要：關於 zbar

程式使用 pyzbar 進行 QR code 偵測。在 Windows ARM 上：

### 選項 1: 使用 Miniconda（最推薦）

1. 安裝 Miniconda for ARM64
   - https://docs.conda.io/en/latest/miniconda.html
   - 選擇 Windows ARM64 版本

2. 安裝 zbar
   ```bash
   conda install -c conda-forge zbar
   ```

3. 在 Anaconda Prompt 中執行程式
   ```bash
   python qrcode_converter.py
   ```

### 選項 2: 不安裝 zbar（使用 OpenCV）

程式會自動偵測 zbar 是否可用：
- **有 zbar**: 使用 pyzbar（準確度高，推薦）
- **沒有 zbar**: 自動使用 OpenCV（準確度略低但仍可用）

**注意**: Windows ARM 上手動安裝 zbar DLL 較為複雜，建議使用 Miniconda 方式。

## 📁 檔案結構

```
release-windows-arm/
├── qrcode_converter.py          # 主程式
├── run.bat                       # 執行程式（雙擊）
├── install.bat                   # 安裝套件（雙擊）
├── requirements.txt              # Python 套件清單
├── Windows_ARM_使用說明.txt     # 本檔案
├── input/                        # 放置原始 QR code 圖片
└── output/                       # 轉換後的輸出位置
```

## 🎮 使用範例

### 範例 1: 單張圖片，單個 QR code
```
input/
  └── qrcode1.jpg  → output/qrcode1.jpg
```

### 範例 2: 單張圖片，3 個 QR code
```
input/
  └── receipt.jpg  → output/receipt_1.jpg
                   → output/receipt_2.jpg
                   → output/receipt_3.jpg
```

### 範例 3: 批次處理
```
input/
  ├── photo1.jpg  → output/photo1_1.jpg, photo1_2.jpg, photo1_3.jpg
  ├── photo2.jpg  → output/photo2_1.jpg, photo2_2.jpg, photo2_3.jpg
  └── photo3.jpg  → output/photo3_1.jpg, photo3_2.jpg, photo3_3.jpg
```

## 🔧 疑難排解

### 問題 1: 找不到 Python
**解決方法**:
1. 確認已安裝 Python ARM64 版本
2. 重新安裝時勾選「Add Python to PATH」
3. 重新啟動電腦

### 問題 2: pip 安裝套件失敗
**解決方法**:
```bash
# 方法 1: 更新 pip
python -m pip install --upgrade pip

# 方法 2: 使用 --user 選項
pip install --user -r requirements.txt

# 方法 3: 使用管理員權限
以系統管理員身分執行 cmd
```

### 問題 3: 無法偵測 QR code
**解決方法**:
1. 使用 Miniconda 安裝 zbar（見上方說明）
2. 確認圖片清晰、品質良好
3. 檢查 QR code 沒有損壞或變形
4. 如果只偵測到部分 QR code，檢查 incomplete_files_report.txt

### 問題 4: 偵測數量不足 3 個
程式會自動生成 `incomplete_files_report.txt` 報告：
- 列出偵測不完整的檔案
- 顯示偵測到的數量
- 可能原因：圖片品質、QR code 損壞

### 問題 5: 程式執行後立即關閉
**解決方法**:
- 使用 `run.bat` 執行（會暫停等待）
- 或在 cmd 中手動執行: `python qrcode_converter.py`

## 💡 效能優化建議

1. **圖片品質**: 使用高解析度、清晰的圖片
2. **批次處理**: 一次處理多個檔案更有效率
3. **安裝 zbar**: 大幅提升偵測準確度和速度

## 🌟 為何不使用 .exe？

在 Windows ARM 上：
- PyInstaller 對 ARM64 支援有限
- 直接使用 Python 腳本更穩定
- 更容易更新和維護
- 體積更小、啟動更快

## 📞 技術支援

遇到問題時的檢查清單：
1. ✓ Python 版本是否為 ARM64 版本？
2. ✓ 是否已執行 install.bat？
3. ✓ 圖片是否放在 input 資料夾？
4. ✓ 圖片格式是否支援？
5. ✓ 是否有查看 incomplete_files_report.txt？

---

版本: 1.0 (Windows ARM 優化版)
日期: 2025-11-01

推薦使用 Miniconda + zbar 以獲得最佳效果！
"""
    
    readme_path = release_folder / 'Windows_ARM_使用說明.txt'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ 已建立: Windows_ARM_使用說明.txt")


def create_run_bat(release_folder):
    """建立執行批次檔"""
    content = """@echo off
chcp 65001 >nul
title QR Code 轉換程式
color 0A

echo.
echo ╔════════════════════════════════════════════════╗
echo ║       QR Code 轉換程式 - Windows ARM 版       ║
echo ║         將 [CVS] 轉換為 [MyCard]             ║
echo ╚════════════════════════════════════════════════╝
echo.

REM 檢查 Python 是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 Python！
    echo.
    echo 請先安裝 Python for Windows ARM64:
    echo https://www.python.org/downloads/windows/
    echo.
    echo 安裝時記得勾選「Add Python to PATH」
    echo.
    pause
    exit /b 1
)

echo [提示] Python 已安裝
python --version
echo.

REM 檢查必要套件
python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo [警告] 必要套件未安裝！
    echo.
    echo 請先執行 install.bat 安裝套件
    echo 或手動執行: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [提示] 套件已安裝
echo.

REM 檢查 input 資料夾
if not exist "input" (
    mkdir input
    echo [提示] 已建立 input 資料夾
)

REM 檢查是否有圖片檔案
dir /b input\*.jpg input\*.png input\*.jpeg input\*.bmp input\*.gif input\*.tiff >nul 2>&1
if errorlevel 1 (
    echo [提示] input 資料夾中沒有圖片檔案
    echo.
    echo 請將 QR code 圖片放入 input 資料夾後再執行
    echo 支援格式: JPG, PNG, JPEG, BMP, GIF, TIFF
    echo.
    pause
    exit /b 0
)

echo ════════════════════════════════════════════════
echo 開始處理 QR code...
echo ════════════════════════════════════════════════
echo.

REM 執行程式
python qrcode_converter.py

echo.
echo ════════════════════════════════════════════════
echo 處理完成！
echo ════════════════════════════════════════════════
echo.
echo 請查看 output 資料夾中的轉換結果
echo.
if exist incomplete_files_report.txt (
    echo [提示] 發現偵測不完整報告，請查看:
    echo         incomplete_files_report.txt
    echo.
)

pause
"""
    
    bat_path = release_folder / 'run.bat'
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ 已建立: run.bat")


def create_install_bat(release_folder):
    """建立安裝批次檔"""
    content = """@echo off
chcp 65001 >nul
title 安裝 QR Code 轉換程式所需套件
color 0B

echo.
echo ╔════════════════════════════════════════════════╗
echo ║          安裝 QR Code 轉換程式套件            ║
echo ╚════════════════════════════════════════════════╝
echo.

REM 檢查 Python 是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 Python！
    echo.
    echo 請先從以下網址下載並安裝 Python for Windows ARM64:
    echo https://www.python.org/downloads/windows/
    echo.
    echo 安裝時務必勾選「Add Python to PATH」選項！
    echo.
    pause
    exit /b 1
)

echo [✓] Python 已安裝
python --version
echo.

echo ════════════════════════════════════════════════
echo 正在更新 pip...
echo ════════════════════════════════════════════════
python -m pip install --upgrade pip
echo.

echo ════════════════════════════════════════════════
echo 正在安裝套件...（這可能需要幾分鐘）
echo ════════════════════════════════════════════════
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [錯誤] 套件安裝失敗！
    echo.
    echo 請嘗試以下解決方法:
    echo 1. 以系統管理員身分執行此批次檔
    echo 2. 手動執行: pip install --user -r requirements.txt
    echo 3. 安裝 Miniconda 並使用 conda 安裝
    echo.
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════
echo ✅ 安裝完成！
echo ════════════════════════════════════════════════
echo.
echo 已安裝的套件:
pip list | findstr "opencv qrcode Pillow pyzbar"
echo.

echo ════════════════════════════════════════════════
echo 關於 pyzbar (QR code 偵測):
echo ════════════════════════════════════════════════
echo.

python -c "from pyzbar.pyzbar import decode; print('[✓] pyzbar 可正常使用')" 2>nul
if errorlevel 1 (
    echo [!] pyzbar 已安裝但可能缺少 zbar 函式庫
    echo.
    echo 程式仍可執行，會自動使用 OpenCV 偵測器
    echo （準確度略低但仍可使用）
    echo.
    echo 如需最佳效果，建議安裝 Miniconda 並執行:
    echo   conda install -c conda-forge zbar
    echo.
) else (
    echo [✓] pyzbar 可正常使用！
    echo.
)

echo ════════════════════════════════════════════════
echo 下一步:
echo ════════════════════════════════════════════════
echo 1. 將 QR code 圖片放入 input 資料夾
echo 2. 雙擊 run.bat 執行程式
echo 3. 查看 output 資料夾中的轉換結果
echo.

pause
"""
    
    bat_path = release_folder / 'install.bat'
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ 已建立: install.bat")


if __name__ == "__main__":
    create_windows_arm_package()

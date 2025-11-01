# 如何在 Windows 上使用 QR Code 轉換程式

## 📦 發布套件說明

`release` 資料夾包含了所有需要的檔案，可以直接複製到 Windows 電腦使用。

## 🚀 Windows 使用方法

### 方法 1: 使用 Python 腳本（推薦，最可靠）

1. **安裝 Python**
   - 下載並安裝 Python 3.8 或更新版本
   - 官網：https://www.python.org/downloads/
   - 安裝時記得勾選「Add Python to PATH」

2. **複製 release 資料夾到 Windows 電腦**

3. **安裝相依套件**
   - 開啟命令提示字元（CMD）或 PowerShell
   - 進入 release 資料夾
   - 執行：`pip install -r requirements.txt`

4. **執行程式**
   - 雙擊 `run.bat` 即可
   - 或在命令提示字元執行：`python qrcode_converter.py`

5. **放入圖片並處理**
   - 將 QR code 圖片放入 `input` 資料夾
   - 執行程式
   - 查看 `output` 資料夾中的結果

### 方法 2: 使用可執行檔（需要在 Windows 上重新打包）

由於你目前在 macOS 上，生成的是 macOS 版本的可執行檔。
要在 Windows 上使用可執行檔，需要：

1. 將整個專案複製到 Windows 電腦
2. 在 Windows 上安裝 Python 和 PyInstaller
3. 執行 `python build_windows.py`
4. 會生成 `QRCodeConverter.exe`

## ⚠️ 重要：安裝 zbar

為了更好的 QR code 偵測效果，建議安裝 zbar：

### 選項 1: 使用 Conda（最簡單）
```bash
conda install -c conda-forge zbar
```

### 選項 2: 手動下載 DLL
1. 下載 zbar for Windows：http://zbar.sourceforge.net/download.html
2. 解壓縮後找到 `libzbar-64.dll`
3. 將 DLL 複製到程式目錄中

### 選項 3: 不安裝（使用 OpenCV）
程式會自動回退到 OpenCV 偵測器，但準確度會稍低。

## 📁 檔案說明

```
release/
├── qrcode_converter.py          # 主程式（Python 腳本）
├── run.bat                       # Windows 批次檔（雙擊執行）
├── requirements.txt              # Python 套件清單
├── Windows使用說明.txt          # Windows 使用說明
├── README.md                     # 完整說明文件
├── input/                        # 放置原始 QR code 圖片
└── output/                       # 轉換後的 QR code 輸出位置
```

## 🔧 疑難排解

### 問題 1: 找不到 Python
- 確認已安裝 Python
- 確認安裝時勾選了「Add Python to PATH」
- 重新開機後再試

### 問題 2: pip 安裝套件失敗
- 使用管理員權限執行命令提示字元
- 或使用：`pip install --user -r requirements.txt`

### 問題 3: 無法偵測 QR code
- 安裝 zbar（見上方說明）
- 確認圖片品質良好
- 檢查 QR code 是否清晰

### 問題 4: 程式執行後立即關閉
- 使用 `run.bat` 執行
- 或在 CMD 中手動執行 `python qrcode_converter.py`

## 💡 使用技巧

1. **批次處理**
   - 可以一次在 input 資料夾放入多張圖片
   - 程式會自動處理所有圖片

2. **檢查報告**
   - 執行完成後檢查 `incomplete_files_report.txt`
   - 查看哪些圖片沒有偵測到 3 個 QR code

3. **重複執行**
   - output 資料夾會在每次執行前自動清空
   - 不用手動刪除舊檔案

## 📞 技術支援

如遇到問題：
1. 查看 `Windows使用說明.txt`
2. 查看 `README.md`
3. 檢查 Python 版本：`python --version`（需要 3.8+）
4. 檢查套件是否安裝：`pip list`

---

建議：在 Windows 上使用 Python 腳本方式（方法 1）最為穩定可靠！

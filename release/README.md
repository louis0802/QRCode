# QR Code 轉換程式

這是一個用於批次處理 QR code 的 Python 程式，可以讀取資料夾中的 QR code 圖片，將內容從 `[CVS]` 轉換為 `[MyCard]`，然後生成新的 QR code。

## 功能特色

- 📖 自動讀取 `input` 資料夾中的所有 QR code 圖片
- 🔄 將內容中的 `[CVS]` 替換為 `[MyCard]`
- 💾 生成新的 QR code 並儲存到 `output` 資料夾
- 🖼️ 支援多種圖片格式：PNG, JPG, JPEG, BMP, GIF, TIFF
- ✅ 詳細的處理狀態顯示

## 安裝步驟

### 1. 確保已安裝 Python

需要 Python 3.7 或更新版本。檢查 Python 版本：

```bash
python3 --version
```

### 2. 安裝相依套件

在專案目錄下執行：

```bash
pip3 install -r requirements.txt
```

或手動安裝：

```bash
pip3 install opencv-python qrcode[pil] Pillow
```

## 使用方法

### 1. 準備 QR code 圖片

將要處理的 QR code 圖片放入 `input` 資料夾中。

例如：
```
input/
  ├── qrcode1.png
  ├── qrcode2.jpg
  └── qrcode3.png
```

### 2. 執行程式

在專案目錄下執行：

```bash
python3 qrcode_converter.py
```

### 3. 查看結果

處理完成後，轉換後的 QR code 會儲存在 `output` 資料夾中，檔名與原始檔案相同。

```
output/
  ├── qrcode1.png
  ├── qrcode2.jpg
  └── qrcode3.png
```

## 範例

### 輸入 QR code 內容
```
[CVS]|MAVVLQ041597|5HVW486G4LV8
```

### 輸出 QR code 內容
```
[MyCard]|MAVVLQ041597|5HVW486G4LV8
```

## 執行範例輸出

```
QR Code 轉換程式
將 [CVS] 轉換為 [MyCard]
============================================================
找到 3 個圖片檔案
============================================================

處理中: qrcode1.png
  原始內容: [CVS]|MAVVLQ041597|5HVW486G4LV8
  轉換內容: [MyCard]|MAVVLQ041597|5HVW486G4LV8
  ✅ 成功儲存到: output/qrcode1.png

處理中: qrcode2.png
  原始內容: [CVS]|TEST123456|ABCD1234
  轉換內容: [MyCard]|TEST123456|ABCD1234
  ✅ 成功儲存到: output/qrcode2.png

處理中: qrcode3.png
  原始內容: [CVS]|SAMPLE789|XYZ9876
  轉換內容: [MyCard]|SAMPLE789|XYZ9876
  ✅ 成功儲存到: output/qrcode3.png

============================================================
處理完成！
✅ 成功: 3 個
❌ 失敗: 0 個
輸出資料夾: /Users/louis/Documents/Projects/mycard-qrcode/output
```

## 專案結構

```
mycard-qrcode/
├── qrcode_converter.py    # 主程式
├── requirements.txt       # Python 套件清單
├── README.md             # 說明文件
├── input/                # 輸入資料夾（放置原始 QR code 圖片）
└── output/               # 輸出資料夾（儲存轉換後的 QR code）
```

## 相依套件

- **opencv-python**: 用於讀取和解碼 QR code 圖片
- **qrcode**: 用於生成新的 QR code
- **Pillow**: 圖片處理函式庫（qrcode 的相依套件）

## 常見問題

### Q: 無法讀取 QR code？
A: 請確保：
- 圖片品質良好，QR code 清晰可見
- QR code 沒有損壞或變形
- 圖片格式為支援的格式（PNG, JPG 等）

### Q: 程式找不到圖片？
A: 請確認：
- 圖片已放置在 `input` 資料夾中
- 圖片副檔名是支援的格式
- 檔案權限允許讀取

### Q: 如何調整生成的 QR code 品質？
A: 可以修改 `qrcode_converter.py` 中的參數：
- `box_size`: 調整每個格子的像素大小
- `border`: 調整邊框寬度
- `error_correction`: 調整容錯率

## 授權

此專案為個人使用工具程式。

## 聯絡方式

如有問題或建議，歡迎提出。

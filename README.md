# QR Code 轉換程式

這是一個用於批次處理 QR code 的 Python 程式，可以讀取資料夾中的 QR code 圖片，將內容從 `[CVS]` 轉換為 `[MyCard]`，然後生成新的 QR code。

## ✨ 功能特色

- 🌐 **網頁介面**：簡單直覺的 Streamlit 網頁應用
- 📖 自動讀取多個 QR code（支援單張圖片包含多個 QR code）
- 🔄 將內容中的 `[CVS]` 替換為 `[MyCard]`
- 💾 生成新的 QR code 並提供下載
- 🖼️ 支援多種圖片格式：PNG, JPG, JPEG, BMP, GIF, TIFF
- 🐳 支援 Docker 和 Kubernetes 部署
- 📊 批次處理和即時預覽

## 🚀 快速開始

### 選擇你的使用方式

#### 1️⃣ 網頁版（推薦）

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動網頁應用
streamlit run web_app.py

# 在瀏覽器訪問: http://localhost:8501
```

#### 2️⃣ 命令列版

```bash
# 安裝依賴
pip install -r requirements.txt

# 將 QR code 圖片放入 input 資料夾
# 然後執行
python qrcode_converter.py

# 結果會在 output 資料夾
```

#### 3️⃣ Docker 版

```bash
# 使用 Docker Compose（最簡單）
docker-compose up -d

# 訪問: http://localhost:8501
```

#### 4️⃣ Kubernetes 版

```bash
# 快速部署
kubectl apply -f k8s/

# 本地訪問
kubectl port-forward svc/qrcode-converter 8501:80
```

📖 **詳細部署指南**：
- [快速開始指南](QUICKSTART.md) - 最快速的部署方式
- [完整部署指南](DEPLOYMENT.md) - Docker 和 Kubernetes 詳細說明

## 📦 部署選項

| 方式 | 適用場景 | 優點 |
|------|---------|------|
| **本地運行** | 個人使用、開發測試 | 簡單快速 |
| **Docker** | 開發環境、小規模部署 | 環境一致性 |
| **Kubernetes** | 生產環境、高可用性 | 自動擴展、負載平衡 |
| **Streamlit Cloud** | 快速分享、免費托管 | 零成本、自動更新 |

## 🛠️ 使用 Makefile（推薦）

```bash
# 查看所有可用命令
make help

# 常用命令
make run-local           # 本地運行
make docker-compose-up   # Docker 啟動
make deploy-k8s          # Kubernetes 部署
make k8s-logs            # 查看日誌
```

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
├── qrcode_converter.py       # 核心轉換邏輯
├── web_app.py                # Streamlit 網頁應用
├── requirements.txt          # Python 套件清單
├── Dockerfile                # Docker 映像定義
├── docker-compose.yml        # Docker Compose 配置
├── .dockerignore            # Docker 忽略檔案
├── Makefile                 # 快速命令工具
├── deploy.sh                # 自動化部署腳本
├── README.md                # 專案說明
├── QUICKSTART.md            # 快速開始指南
├── DEPLOYMENT.md            # 完整部署指南
├── input/                   # 輸入資料夾（CLI 模式）
├── output/                  # 輸出資料夾（CLI 模式）
└── k8s/                     # Kubernetes 配置
    ├── deployment.yaml      # Deployment 配置
    ├── service.yaml         # Service 配置
    ├── ingress.yaml         # Ingress 配置
    ├── configmap.yaml       # ConfigMap 配置
    └── hpa.yaml            # 自動擴展配置
```

## 📚 文件說明

- **[README.md](README.md)** - 專案概述和基本使用（你正在看的）
- **[QUICKSTART.md](QUICKSTART.md)** - 快速開始和常用命令
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - 詳細的 Docker 和 K8s 部署指南

## 🎯 使用場景

### 網頁版使用流程

1. 打開瀏覽器訪問應用
2. 選擇「單張上傳」或「批次上傳」模式
3. 上傳包含 QR code 的圖片
4. 自動檢測並轉換所有 QR code
5. 即時預覽和下載轉換後的 QR code

### 命令列版使用流程

1. 將 QR code 圖片放入 `input` 資料夾
2. 執行 `python qrcode_converter.py`
3. 在 `output` 資料夾查看結果

## 相依套件

### 核心套件
- **opencv-python**: 用於讀取和解碼 QR code 圖片
- **pyzbar**: 增強的 QR code 檢測（需要 libzbar0 系統庫）
- **qrcode**: 用於生成新的 QR code
- **Pillow**: 圖片處理函式庫
- **streamlit**: 網頁應用框架

### 系統依賴（Docker 自動安裝）
- libzbar0: QR code 檢測庫
- libgl1-mesa-glx: OpenCV 圖形庫

## 🔧 進階功能

### 多 QR code 檢測

程式使用 5 層檢測策略來確保最高的檢測率：
1. pyzbar 原始圖片檢測
2. pyzbar 灰階圖片檢測
3. pyzbar CLAHE 增強檢測
4. pyzbar 二值化檢測
5. OpenCV QRCodeDetector 檢測

### Docker 健康檢查

容器自動監控健康狀態：
```bash
# 查看健康狀態
docker inspect --format='{{json .State.Health}}' qrcode-converter
```

### Kubernetes 自動擴展

根據 CPU 和記憶體使用自動調整副本數（2-10 個）：
```bash
# 查看 HPA 狀態
kubectl get hpa qrcode-converter
```

## 🌐 生產環境部署

### 使用自動化腳本

```bash
# 設定 Registry
export REGISTRY=your-registry.com/username

# 執行部署
./deploy.sh v1.0.0
```

### 使用 Makefile

```bash
# 設定變數
export REGISTRY=your-registry.com/username
export VERSION=v1.0.0

# 完整部署流程
make deploy-k8s

# 更新應用
make k8s-update

# 查看狀態
make k8s-status
make k8s-logs
```

### 配置 HTTPS

使用 cert-manager 自動獲取 Let's Encrypt 證書：
```bash
# 詳細步驟見 DEPLOYMENT.md
kubectl apply -f k8s/ingress.yaml
```

## 📊 監控和維護

```bash
# 查看資源使用
make k8s-top

# 查看日誌
make k8s-logs

# 擴展副本
make k8s-scale REPLICAS=5

# 重啟應用
make k8s-restart

# 回滾版本
make k8s-rollback
```

## 常見問題

### Q: 無法讀取 QR code？
A: 程式使用 5 層檢測策略，應該能檢測大部分 QR code。如果仍無法讀取：
- 確保圖片品質良好，QR code 清晰可見
- 嘗試調整圖片亮度或對比度
- 確認 QR code 沒有嚴重損壞或變形

### Q: 網頁版無法啟動？
A: 檢查：
- Python 版本是否 3.7+
- 所有依賴是否已安裝：`pip install -r requirements.txt`
- 端口 8501 是否被占用
- 查看錯誤訊息並參考 DEPLOYMENT.md

### Q: Docker 容器無法啟動？
A: 
```bash
# 查看日誌
docker logs qrcode-converter

# 常見問題：
# - 端口衝突：修改 docker-compose.yml 中的端口
# - 記憶體不足：增加 Docker 資源限制
# - 映像損壞：重新建立映像 make docker-build
```

### Q: Kubernetes Pod 一直重啟？
A:
```bash
# 查看詳細狀態
make k8s-describe

# 查看日誌
make k8s-logs

# 常見原因：
# - 映像拉取失敗：檢查 Registry 憑證
# - 資源不足：調整 resources 限制
# - 健康檢查失敗：檢查應用是否正常啟動
```

### Q: 如何調整生成的 QR code 品質？
A: 可以修改 `qrcode_converter.py` 中的參數：
```python
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # 容錯率
    box_size=10,  # 每個格子的像素大小
    border=4,     # 邊框寬度
)
```

### Q: 支援哪些雲平台？
A: 
- **Kubernetes**: 任何 K8s 集群（GKE, EKS, AKS, 自建）
- **Docker**: 支援所有支援 Docker 的平台
- **Streamlit Cloud**: 免費托管（見 DEPLOYMENT.md）
- **雲端服務**: AWS, GCP, Azure（見 DEPLOYMENT.md）

### Q: 如何擴展應用以處理大量請求？
A:
```bash
# Kubernetes 自動擴展（推薦）
kubectl apply -f k8s/hpa.yaml

# 手動擴展
make k8s-scale REPLICAS=10

# 調整資源限制
# 編輯 k8s/deployment.yaml 的 resources 部分
```

## 🔒 安全性考量

### 生產環境建議

1. **使用 HTTPS**：配置 TLS 證書（見 DEPLOYMENT.md）
2. **限制網路訪問**：使用 Kubernetes NetworkPolicy
3. **資源限制**：設定適當的 CPU 和記憶體限制
4. **定期更新**：保持基礎映像和依賴套件更新
5. **監控日誌**：集成日誌收集和告警系統

## 🤝 貢獻

歡迎提出問題和改進建議！

## 📄 授權

此專案為個人使用工具程式。

## 🎉 致謝

感謝以下開源專案：
- Streamlit - 網頁應用框架
- OpenCV - 電腦視覺庫
- pyzbar - QR code 檢測
- qrcode - QR code 生成

---

**快速鏈接：**
- 📖 [快速開始](QUICKSTART.md)
- 🚀 [部署指南](DEPLOYMENT.md)
- 🐛 [問題回報](https://github.com/your-repo/issues)

**需要幫助？**
1. 查看 [快速開始指南](QUICKSTART.md)
2. 閱讀 [完整部署文檔](DEPLOYMENT.md)
3. 運行 `make help` 查看可用命令

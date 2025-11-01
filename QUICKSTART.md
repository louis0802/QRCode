# 🚀 快速開始指南

> 用最快的方式部署你的 QRCode 轉換器！

## 📋 選擇部署方式

### 1️⃣ 本地測試（最簡單）

```bash
# 安裝依賴
pip install -r requirements.txt

# 運行應用
streamlit run web_app.py

# 訪問: http://localhost:8501
```

### 2️⃣ Docker 部署（推薦用於開發）

```bash
# 使用 Docker Compose（一鍵啟動）
docker-compose up -d

# 訪問: http://localhost:8501
```

**或使用 Makefile：**
```bash
make deploy-local
```

### 3️⃣ Kubernetes 部署（生產環境）

#### 前提條件
- ✅ Kubernetes 集群已就緒
- ✅ kubectl 已配置
- ✅ Docker Registry 帳號

#### 快速部署

```bash
# 1. 設定 Registry（編輯這些檔案）
# - Makefile: 修改 REGISTRY 變數
# - deploy.sh: 修改 REGISTRY 變數
# - k8s/deployment.yaml: 修改 image 地址

# 2. 一鍵部署
./deploy.sh v1.0.0

# 3. 訪問應用
kubectl port-forward svc/qrcode-converter 8501:80
```

**或使用 Makefile：**
```bash
# 設定環境變數
export REGISTRY=your-registry
export VERSION=v1.0.0

# 完整部署（建立 + 推送 + 部署）
make deploy-k8s

# 本地訪問
make k8s-port-forward
```

## 🛠️ 使用 Makefile（推薦）

查看所有可用命令：
```bash
make help
```

### 常用命令

#### 本地開發
```bash
make run-local          # 運行本地應用
make install            # 安裝依賴
```

#### Docker 操作
```bash
make docker-build       # 建立映像
make docker-run         # 運行容器
make docker-logs        # 查看日誌
make docker-stop        # 停止容器
make docker-push        # 推送到 Registry

# Docker Compose
make docker-compose-up  # 啟動
make docker-compose-down # 停止
```

#### Kubernetes 操作
```bash
make k8s-apply          # 部署
make k8s-status         # 查看狀態
make k8s-logs           # 查看日誌
make k8s-port-forward   # 本地訪問
make k8s-update         # 更新部署
make k8s-delete         # 刪除部署
```

## 🎯 典型工作流程

### 開發流程

```bash
# 1. 本地開發測試
make run-local

# 2. 測試 Docker 版本
make docker-compose-up
make docker-compose-logs

# 3. 完成後清理
make docker-compose-down
```

### 部署到生產環境

```bash
# 設定變數
export REGISTRY=your-registry.com/username
export VERSION=v1.0.0

# 方案 A: 使用自動化腳本
./deploy.sh $VERSION

# 方案 B: 使用 Makefile
make deploy-k8s VERSION=$VERSION

# 訪問應用
make k8s-port-forward
# 或配置 Ingress 後直接訪問域名
```

### 更新應用

```bash
# 1. 修改代碼後

# 2. 更新版本號
export VERSION=v1.0.1

# 3. 建立新映像並部署
make k8s-update VERSION=$VERSION

# 4. 查看更新狀態
make k8s-status
```

## 📊 監控和維護

```bash
# 查看資源使用
make k8s-top

# 查看詳細日誌
make k8s-logs

# 查看事件
make k8s-events

# 進入容器 Shell
make k8s-shell

# 擴展副本數
make k8s-scale REPLICAS=5

# 重啟應用
make k8s-restart
```

## 🐛 故障排除

### Docker 問題

```bash
# 映像建立失敗
make docker-build  # 查看建立日誌

# 容器無法啟動
make docker-logs   # 查看運行日誌

# 清理並重新開始
make clean
make docker-build
```

### Kubernetes 問題

```bash
# Pod 無法啟動
make k8s-describe  # 查看詳細資訊
make k8s-logs      # 查看日誌

# 映像拉取失敗
# 1. 檢查 Registry 地址是否正確
# 2. 確認已登入 Registry: docker login <registry>
# 3. 重新推送映像: make docker-push

# 回滾到上一版本
make k8s-rollback
```

## 🌐 訪問方式總結

### 本地開發
- **Streamlit 直接運行**: http://localhost:8501
- **Docker**: http://localhost:8501

### Kubernetes

#### Port Forward（測試）
```bash
make k8s-port-forward
# 訪問: http://localhost:8501
```

#### Ingress（生產）
1. 確保 Ingress Controller 已安裝
2. 配置 DNS 指向 Ingress IP
3. 訪問: http://qrcode-converter.yourdomain.com

#### NodePort（無 Ingress）
```bash
# 修改 Service 類型為 NodePort
kubectl patch svc qrcode-converter -p '{"spec":{"type":"NodePort"}}'

# 獲取訪問地址
kubectl get svc qrcode-converter
# 訪問: http://<node-ip>:<node-port>
```

## 📝 配置檔案說明

| 檔案 | 用途 |
|------|------|
| `Dockerfile` | Docker 映像定義 |
| `docker-compose.yml` | Docker Compose 配置 |
| `k8s/deployment.yaml` | Kubernetes Deployment |
| `k8s/service.yaml` | Kubernetes Service |
| `k8s/ingress.yaml` | Kubernetes Ingress |
| `k8s/hpa.yaml` | 自動擴展配置 |
| `Makefile` | 常用命令快捷方式 |
| `deploy.sh` | 自動化部署腳本 |

## 🎓 進階主題

詳細資訊請參考：
- 📖 [完整部署指南](DEPLOYMENT.md) - Docker 和 Kubernetes 詳細說明
- 🚀 [雲端部署](DEPLOYMENT.md#️-雲端部署方案) - Streamlit Cloud、AWS、GCP、Azure 部署

## ❓ 需要幫助？

1. 查看完整文檔：[DEPLOYMENT.md](DEPLOYMENT.md)
2. 查看可用命令：`make help`
3. 查看腳本幫助：`./deploy.sh -h`

## 🎉 就這麼簡單！

選擇最適合你的方式：
- 🏠 本地測試？用 `streamlit run web_app.py`
- 🐳 Docker？用 `docker-compose up -d`
- ☸️ Kubernetes？用 `./deploy.sh` 或 `make deploy-k8s`

Happy deploying! 🚀

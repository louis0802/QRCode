# QR Code 轉換器 - 完整部署指南

## 📋 目錄
- [本地測試](#本地測試)
- [Docker 部署](#-docker-部署)
- [Kubernetes 部署](#️-kubernetes-部署)
- [雲端部署方案](#️-雲端部署方案)

## 🌐 本地測試

### 本地訪問
- **本地網址**: http://localhost:8501
- **網路網址**: http://192.168.1.3:8501 （區域網路內其他設備可訪問）

## 🐳 Docker 部署

### 前提條件
- Docker 已安裝（20.10+）
- Docker Compose 已安裝（可選，用於簡化部署）

### 快速開始

#### 方法 1: 使用 Docker Compose（推薦）

```bash
# 啟動服務
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down

# 訪問應用
open http://localhost:8501
```

#### 方法 2: 使用 Docker 命令

```bash
# 建立映像
docker build -t qrcode-converter:latest .

# 運行容器
docker run -d \
  -p 8501:8501 \
  --name qrcode-converter \
  --restart unless-stopped \
  qrcode-converter:latest

# 查看日誌
docker logs -f qrcode-converter

# 停止容器
docker stop qrcode-converter

# 刪除容器
docker rm qrcode-converter
```

### 映像管理

#### 建立和標記

```bash
# 建立映像
docker build -t qrcode-converter:latest .

# 標記映像（準備推送到 registry）
docker tag qrcode-converter:latest <your-registry>/qrcode-converter:latest
docker tag qrcode-converter:latest <your-registry>/qrcode-converter:v1.0.0
```

#### 推送到 Docker Registry

```bash
# Docker Hub
docker login
docker push <your-username>/qrcode-converter:latest

# 私有 Registry
docker login <your-registry>
docker push <your-registry>/qrcode-converter:latest
```

### 驗證部署

```bash
# 檢查容器狀態
docker ps | grep qrcode-converter

# 查看容器資源使用
docker stats qrcode-converter

# 進入容器（除錯用）
docker exec -it qrcode-converter /bin/bash

# 查看容器詳細資訊
docker inspect qrcode-converter
```

### Docker 故障排除

```bash
# 容器無法啟動
docker logs qrcode-converter

# 檢查健康狀態
docker inspect --format='{{json .State.Health}}' qrcode-converter

# 重新建立映像（清除快取）
docker build --no-cache -t qrcode-converter:latest .

# 清理未使用的映像
docker system prune -a
```

## ☸️ Kubernetes 部署

### 前提條件

- Kubernetes 集群（v1.20+）
- kubectl 已配置並連接到集群
- （可選）Ingress Controller（如 nginx-ingress-controller）
- （可選）Metrics Server（用於 HPA 自動擴展）

### 部署架構

```
┌─────────────┐
│   Ingress   │ (可選 - 外部訪問)
└──────┬──────┘
       │
┌──────▼──────┐
│   Service   │ (ClusterIP)
└──────┬──────┘
       │
┌──────▼──────┐
│ Deployment  │ (2-10 Pods with HPA)
│   + Pods    │
└─────────────┘
```

### 快速部署

```bash
# 1. 更新映像地址（如果使用私有 registry）
# 編輯 k8s/deployment.yaml
# 將 image: qrcode-converter:latest 改為 <your-registry>/qrcode-converter:latest

# 2. 一鍵部署所有資源
kubectl apply -f k8s/

# 3. 查看部署狀態
kubectl get all -l app=qrcode-converter

# 4. 等待 Pods 準備就緒
kubectl wait --for=condition=ready pod -l app=qrcode-converter --timeout=300s
```

### 逐步部署

#### 1. ConfigMap（配置）

```bash
kubectl apply -f k8s/configmap.yaml

# 驗證
kubectl get configmap qrcode-converter-config
kubectl describe configmap qrcode-converter-config
```

#### 2. Deployment（應用部署）

```bash
kubectl apply -f k8s/deployment.yaml

# 查看部署狀態
kubectl rollout status deployment/qrcode-converter

# 查看 Pods
kubectl get pods -l app=qrcode-converter -o wide

# 查看 Pod 詳情
kubectl describe pod -l app=qrcode-converter
```

#### 3. Service（服務）

```bash
kubectl apply -f k8s/service.yaml

# 驗證 Service
kubectl get svc qrcode-converter

# 檢查 Endpoints
kubectl get endpoints qrcode-converter
```

#### 4. HPA（自動擴展）

```bash
# 確保 Metrics Server 已安裝
kubectl top nodes

# 部署 HPA
kubectl apply -f k8s/hpa.yaml

# 查看 HPA 狀態
kubectl get hpa qrcode-converter

# 持續監控
kubectl get hpa qrcode-converter --watch
```

#### 5. Ingress（外部訪問 - 可選）

```bash
# 編輯 k8s/ingress.yaml，更新域名
# host: qrcode-converter.yourdomain.com

kubectl apply -f k8s/ingress.yaml

# 查看 Ingress
kubectl get ingress qrcode-converter
kubectl describe ingress qrcode-converter

# 獲取 Ingress IP
kubectl get ingress qrcode-converter -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

### 訪問應用

#### 選項 1: Port Forward（測試/開發）

```bash
# 轉發到本地
kubectl port-forward svc/qrcode-converter 8501:80

# 訪問 http://localhost:8501
```

#### 選項 2: NodePort（無 Ingress）

```bash
# 修改 Service 類型
kubectl patch svc qrcode-converter -p '{"spec":{"type":"NodePort"}}'

# 獲取 NodePort
NODE_PORT=$(kubectl get svc qrcode-converter -o jsonpath='{.spec.ports[0].nodePort}')
echo "NodePort: $NODE_PORT"

# 獲取 Node IP
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}')
echo "Access at: http://${NODE_IP}:${NODE_PORT}"
```

#### 選項 3: Ingress（生產環境）

```bash
# 確保 DNS 記錄指向 Ingress Controller IP
# 訪問 http://qrcode-converter.yourdomain.com
```

### 配置 TLS/HTTPS

#### 使用 cert-manager（推薦）

```bash
# 1. 安裝 cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# 2. 建立 ClusterIssuer（Let's Encrypt）
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# 3. 更新 Ingress 使用 cert-manager
# 在 k8s/ingress.yaml 中添加：
# metadata:
#   annotations:
#     cert-manager.io/cluster-issuer: "letsencrypt-prod"
# spec:
#   tls:
#   - hosts:
#     - qrcode-converter.yourdomain.com
#     secretName: qrcode-converter-tls

kubectl apply -f k8s/ingress.yaml
```

#### 使用手動證書

```bash
# 建立 TLS Secret
kubectl create secret tls qrcode-converter-tls \
  --cert=path/to/tls.crt \
  --key=path/to/tls.key

# 在 ingress.yaml 中啟用 TLS（見檔案中的註解）
```

### 監控和維護

#### 查看日誌

```bash
# 所有 Pods 的日誌
kubectl logs -l app=qrcode-converter --tail=100 -f

# 特定 Pod 的日誌
kubectl logs <pod-name> -f

# 之前崩潰的 Pod 日誌
kubectl logs <pod-name> --previous
```

#### 監控資源

```bash
# Pod 資源使用
kubectl top pods -l app=qrcode-converter

# Node 資源使用
kubectl top nodes

# HPA 狀態
kubectl get hpa qrcode-converter --watch

# 事件
kubectl get events --sort-by='.lastTimestamp' | grep qrcode-converter
```

#### 擴展操作

```bash
# 手動擴展
kubectl scale deployment qrcode-converter --replicas=5

# 查看擴展狀態
kubectl get deployment qrcode-converter
kubectl get pods -l app=qrcode-converter
```

### 更新和回滾

#### 滾動更新

```bash
# 1. 建立新版本映像
docker build -t <your-registry>/qrcode-converter:v2.0.0 .
docker push <your-registry>/qrcode-converter:v2.0.0

# 2. 更新 Deployment
kubectl set image deployment/qrcode-converter \
  qrcode-converter=<your-registry>/qrcode-converter:v2.0.0

# 3. 監控更新
kubectl rollout status deployment/qrcode-converter

# 4. 查看歷史
kubectl rollout history deployment/qrcode-converter
```

#### 回滾

```bash
# 回滾到上一版本
kubectl rollout undo deployment/qrcode-converter

# 回滾到特定版本
kubectl rollout undo deployment/qrcode-converter --to-revision=2

# 查看回滾狀態
kubectl rollout status deployment/qrcode-converter
```

### 故障排除

#### Pod 無法啟動

```bash
# 查看 Pod 狀態
kubectl get pods -l app=qrcode-converter
kubectl describe pod <pod-name>

# 常見問題：
# - ImagePullBackOff: 檢查映像地址和 registry 憑證
# - CrashLoopBackOff: 查看日誌找出錯誤
# - Pending: 檢查資源限制和節點可用性

# 檢查映像拉取
kubectl get pods -o jsonpath='{.items[*].status.containerStatuses[*]}'
```

#### 應用無法訪問

```bash
# 檢查 Service
kubectl get svc qrcode-converter
kubectl describe svc qrcode-converter
kubectl get endpoints qrcode-converter

# 檢查 Ingress
kubectl get ingress qrcode-converter
kubectl describe ingress qrcode-converter

# 測試內部連接
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl http://qrcode-converter:80/_stcore/health
```

#### 性能問題

```bash
# 檢查資源使用
kubectl top pods -l app=qrcode-converter

# 調整資源限制（編輯 k8s/deployment.yaml）
# resources:
#   requests:
#     memory: "1Gi"
#     cpu: "500m"
#   limits:
#     memory: "2Gi"
#     cpu: "1000m"

kubectl apply -f k8s/deployment.yaml

# 增加副本數
kubectl scale deployment qrcode-converter --replicas=5
```

### 生產環境最佳實踐

#### 1. 安全性

```bash
# 使用 NetworkPolicy 限制流量
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: qrcode-converter-netpol
spec:
  podSelector:
    matchLabels:
      app: qrcode-converter
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: nginx-ingress
    ports:
    - protocol: TCP
      port: 8501
EOF

# 使用 PodSecurityPolicy（K8s < 1.25）或 Pod Security Standards
```

#### 2. 可靠性

```bash
# PodDisruptionBudget - 確保維護期間的可用性
cat <<EOF | kubectl apply -f -
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: qrcode-converter-pdb
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: qrcode-converter
EOF

# 定期備份配置
kubectl get all,configmap,secret,ingress,pdb -l app=qrcode-converter -o yaml > backup-$(date +%Y%m%d).yaml
```

#### 3. 監控告警（Prometheus + Grafana）

```bash
# 添加 Prometheus annotations 到 Deployment
# metadata:
#   annotations:
#     prometheus.io/scrape: "true"
#     prometheus.io/port: "8501"
#     prometheus.io/path: "/_stcore/metrics"
```

### 清理資源

```bash
# 刪除所有 Kubernetes 資源
kubectl delete -f k8s/

# 或逐個刪除
kubectl delete deployment qrcode-converter
kubectl delete service qrcode-converter
kubectl delete ingress qrcode-converter
kubectl delete hpa qrcode-converter
kubectl delete configmap qrcode-converter-config
kubectl delete pdb qrcode-converter-pdb

# 驗證清理
kubectl get all -l app=qrcode-converter
```

## ☁️ 雲端部署方案

### 選項 1: Streamlit Community Cloud（推薦 - 免費！）

**最簡單、完全免費、自動更新**

#### 步驟：

1. **準備 Git 儲存庫**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **推送到 GitHub**
   ```bash
   # 在 GitHub 建立新儲存庫
   git remote add origin https://github.com/你的使用者名稱/qrcode-converter.git
   git push -u origin main
   ```

3. **部署到 Streamlit Cloud**
   - 前往 https://streamlit.io/cloud
   - 使用 GitHub 帳號登入
   - 點擊 "New app"
   - 選擇你的儲存庫
   - 主檔案: `web_app.py`
   - 點擊 "Deploy"

4. **完成！**
   - 你會得到一個公開網址，例如: `https://你的應用名稱.streamlit.app`
   - 完全免費！
   - 自動 HTTPS
   - 自動更新（push 到 GitHub 就會自動部署）

#### 優點：
- ✅ 完全免費
- ✅ 無需信用卡
- ✅ 自動 HTTPS
- ✅ 自動擴展
- ✅ 簡單易用
- ✅ 自動 CI/CD

#### 限制：
- 資源有限（但對這個應用足夠）
- 閒置後會休眠（首次訪問可能慢）

---

### 選項 2: Render（免費方案）

**也是免費，設定簡單**

#### 步驟：

1. **準備檔案**
   
   建立 `packages.txt`（系統依賴）：
   ```
   libzbar0
   ```

2. **推送到 GitHub**（同上）

3. **部署到 Render**
   - 前往 https://render.com
   - 註冊帳號
   - 點擊 "New +" → "Web Service"
   - 連接 GitHub 儲存庫
   - 設定：
     * Build Command: `pip install -r requirements.txt`
     * Start Command: `streamlit run web_app.py --server.port=$PORT --server.address=0.0.0.0`
   - 點擊 "Create Web Service"

4. **完成！**
   - 獲得 `https://你的應用.onrender.com` 網址

#### 優點：
- ✅ 免費方案可用
- ✅ 自動 HTTPS
- ✅ 較穩定（不休眠）

#### 限制：
- 免費方案有流量限制

---

### 選項 3: Hugging Face Spaces（免費）

**適合 AI/ML 應用，也是免費**

#### 步驟：

1. **前往 Hugging Face**
   - https://huggingface.co/spaces

2. **建立新 Space**
   - 點擊 "Create new Space"
   - 選擇 "Streamlit"
   - 上傳 `web_app.py` 和 `requirements.txt`

3. **完成！**
   - 獲得 `https://huggingface.co/spaces/你的使用者名稱/應用名稱`

---

### 選項 4: Railway（有免費額度）

#### 步驟：

1. **前往 Railway**
   - https://railway.app

2. **連接 GitHub**
   - 授權 Railway 訪問儲存庫

3. **部署**
   - 選擇儲存庫
   - Railway 會自動偵測並部署

#### 優點：
- ✅ 簡單易用
- ✅ 自動部署

#### 限制：
- 每月 $5 免費額度（通常足夠）

---

### 選項 5: 自己的伺服器（VPS）

如果你有自己的伺服器：

```bash
# 安裝依賴
pip install -r requirements.txt

# 使用 systemd 或 supervisor 運行
streamlit run web_app.py --server.port=8501 --server.address=0.0.0.0

# 使用 nginx 作為反向代理
# 配置 SSL 證書（使用 Let's Encrypt）
```

---

## 📝 部署前的準備

### 1. 建立 `.streamlit/config.toml`（可選）

```toml
[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = true
```

### 2. 建立 `packages.txt`（Linux 系統依賴）

```
libzbar0
```

### 3. 建立 `.gitignore`

```
__pycache__/
*.pyc
.DS_Store
*.spec
build/
dist/
input/
output/
incomplete_files_report.txt
.streamlit/secrets.toml
```

---

## 🚀 推薦部署方案

### 對於個人使用：
**→ Streamlit Community Cloud**（最簡單、免費）

### 對於團隊使用：
**→ Render 或 Railway**（更穩定）

### 對於企業使用：
**→ 自己的伺服器 + Docker**（完全控制）

---

## 🔒 安全建議

1. **不要在公開儲存庫中包含敏感資料**
2. **使用環境變數存儲密鑰**（如果需要）
3. **考慮添加身份驗證**（如果處理敏感資料）
4. **限制上傳檔案大小**（已在配置中設定）

---

## 📊 監控和維護

### Streamlit Cloud:
- 內建分析儀表板
- 查看使用量和錯誤

### 其他平台:
- 使用平台提供的監控工具
- 設定告警

---

## 💡 提示

### 提升效能：
```bash
# 安裝 watchdog 以獲得更好的開發體驗
pip install watchdog
```

### 自訂域名：
- 大多數平台支援自訂域名
- 需要在 DNS 設定 CNAME 記錄

### SSL/HTTPS：
- 所有推薦平台都自動提供 HTTPS

---

## 🎯 快速開始（最簡單方式）

```bash
# 1. 建立 GitHub 儲存庫
git init
git add .
git commit -m "QR Code Converter"
git remote add origin https://github.com/你的使用者名稱/qrcode-converter.git
git push -u origin main

# 2. 前往 https://streamlit.io/cloud
# 3. 登入並點擊 "New app"
# 4. 選擇儲存庫和 web_app.py
# 5. 點擊 Deploy

# 完成！你的應用現在在線上了！
```

---

## 📞 需要幫助？

- Streamlit 文件: https://docs.streamlit.io
- Streamlit 論壇: https://discuss.streamlit.io
- Render 文件: https://render.com/docs

---

**恭喜！你的 QR Code 轉換器現在有了網頁版本！** 🎉

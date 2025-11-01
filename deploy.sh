#!/bin/bash

# QRCode Converter - 自動化部署腳本
# 用途：建立 Docker 映像、推送到 Registry、部署到 Kubernetes

set -e  # 遇到錯誤立即退出

# ==================== 配置變數 ====================
REGISTRY="your-registry"          # 替換為你的 Docker Registry（例如：docker.io/username）
IMAGE_NAME="qrcode-converter"
VERSION="${1:-latest}"            # 從命令列參數獲取版本，預設為 latest
NAMESPACE="default"               # Kubernetes namespace

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ==================== 函數定義 ====================

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 未安裝，請先安裝後再運行此腳本"
        exit 1
    fi
}

# ==================== 環境檢查 ====================

print_info "檢查必要工具..."
check_command docker
check_command kubectl

# 檢查 kubectl 連接
if ! kubectl cluster-info &> /dev/null; then
    print_error "kubectl 無法連接到 Kubernetes 集群"
    exit 1
fi

print_info "環境檢查通過 ✓"

# ==================== Docker 建立 ====================

print_info "開始建立 Docker 映像..."
print_info "映像標籤: ${REGISTRY}/${IMAGE_NAME}:${VERSION}"

docker build -t ${IMAGE_NAME}:${VERSION} .

if [ $? -eq 0 ]; then
    print_info "Docker 映像建立成功 ✓"
else
    print_error "Docker 映像建立失敗"
    exit 1
fi

# 標記映像
docker tag ${IMAGE_NAME}:${VERSION} ${REGISTRY}/${IMAGE_NAME}:${VERSION}
docker tag ${IMAGE_NAME}:${VERSION} ${REGISTRY}/${IMAGE_NAME}:latest

print_info "映像已標記: ${REGISTRY}/${IMAGE_NAME}:${VERSION}"
print_info "映像已標記: ${REGISTRY}/${IMAGE_NAME}:latest"

# ==================== Docker 推送 ====================

read -p "是否推送映像到 Registry? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "推送映像到 Registry..."
    
    # 檢查是否已登入
    if ! docker info | grep -q "Username"; then
        print_warn "未檢測到 Docker Registry 登入，請先登入"
        docker login ${REGISTRY}
    fi
    
    docker push ${REGISTRY}/${IMAGE_NAME}:${VERSION}
    docker push ${REGISTRY}/${IMAGE_NAME}:latest
    
    print_info "映像推送成功 ✓"
else
    print_warn "跳過映像推送"
fi

# ==================== Kubernetes 部署 ====================

read -p "是否部署到 Kubernetes? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "開始部署到 Kubernetes..."
    
    # 更新 deployment.yaml 中的映像版本
    print_info "更新 Deployment 配置..."
    
    # 檢查 k8s 目錄是否存在
    if [ ! -d "k8s" ]; then
        print_error "k8s 目錄不存在"
        exit 1
    fi
    
    # 應用所有配置
    print_info "應用 Kubernetes 配置..."
    kubectl apply -f k8s/ -n ${NAMESPACE}
    
    # 更新映像（如果 Deployment 已存在）
    print_info "更新 Deployment 映像..."
    kubectl set image deployment/qrcode-converter \
        qrcode-converter=${REGISTRY}/${IMAGE_NAME}:${VERSION} \
        -n ${NAMESPACE} 2>/dev/null || true
    
    # 等待部署完成
    print_info "等待部署完成..."
    kubectl rollout status deployment/qrcode-converter -n ${NAMESPACE} --timeout=300s
    
    if [ $? -eq 0 ]; then
        print_info "Kubernetes 部署成功 ✓"
    else
        print_error "Kubernetes 部署失敗"
        exit 1
    fi
    
    # 顯示部署狀態
    print_info "部署狀態:"
    echo "----------------------------------------"
    kubectl get all -l app=qrcode-converter -n ${NAMESPACE}
    echo "----------------------------------------"
    
    # 獲取訪問方式
    print_info "應用訪問方式:"
    
    # 檢查 Ingress
    INGRESS_HOST=$(kubectl get ingress qrcode-converter -n ${NAMESPACE} -o jsonpath='{.spec.rules[0].host}' 2>/dev/null)
    if [ ! -z "$INGRESS_HOST" ]; then
        print_info "Ingress URL: http://${INGRESS_HOST}"
    fi
    
    # 顯示 Port Forward 命令
    print_info "本地訪問命令: kubectl port-forward svc/qrcode-converter 8501:80 -n ${NAMESPACE}"
    
else
    print_warn "跳過 Kubernetes 部署"
fi

# ==================== 完成 ====================

echo ""
print_info "=========================================="
print_info "部署完成！"
print_info "映像: ${REGISTRY}/${IMAGE_NAME}:${VERSION}"
print_info "=========================================="
echo ""

# 提示後續操作
print_info "後續操作:"
echo "  1. 查看日誌: kubectl logs -f -l app=qrcode-converter -n ${NAMESPACE}"
echo "  2. 查看狀態: kubectl get pods -l app=qrcode-converter -n ${NAMESPACE}"
echo "  3. 本地訪問: kubectl port-forward svc/qrcode-converter 8501:80 -n ${NAMESPACE}"
echo ""

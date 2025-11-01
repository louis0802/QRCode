# QRCode Converter - Makefile
# 快速執行常用的 Docker 和 Kubernetes 操作

# 配置變數
REGISTRY ?= your-registry
IMAGE_NAME = qrcode-converter
VERSION ?= latest
NAMESPACE ?= default

# 顏色輸出
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m

.PHONY: help
help: ## 顯示幫助資訊
	@echo "$(BLUE)QRCode Converter - 可用命令:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ==================== 本地開發 ====================

.PHONY: run-local
run-local: ## 運行本地 Streamlit 應用
	@echo "$(BLUE)啟動本地應用...$(NC)"
	streamlit run web_app.py

.PHONY: install
install: ## 安裝 Python 依賴
	@echo "$(BLUE)安裝依賴...$(NC)"
	pip install -r requirements.txt

# ==================== Docker 操作 ====================

.PHONY: docker-build
docker-build: ## 建立 Docker 映像
	@echo "$(BLUE)建立 Docker 映像...$(NC)"
	docker build -t $(IMAGE_NAME):$(VERSION) .
	docker tag $(IMAGE_NAME):$(VERSION) $(REGISTRY)/$(IMAGE_NAME):$(VERSION)
	docker tag $(IMAGE_NAME):$(VERSION) $(REGISTRY)/$(IMAGE_NAME):latest
	@echo "$(GREEN)映像建立成功: $(REGISTRY)/$(IMAGE_NAME):$(VERSION)$(NC)"

.PHONY: docker-run
docker-run: ## 運行 Docker 容器
	@echo "$(BLUE)啟動 Docker 容器...$(NC)"
	docker run -d -p 8501:8501 --name $(IMAGE_NAME) $(IMAGE_NAME):$(VERSION)
	@echo "$(GREEN)容器已啟動: http://localhost:8501$(NC)"

.PHONY: docker-stop
docker-stop: ## 停止 Docker 容器
	@echo "$(BLUE)停止容器...$(NC)"
	docker stop $(IMAGE_NAME) || true
	docker rm $(IMAGE_NAME) || true

.PHONY: docker-logs
docker-logs: ## 查看 Docker 容器日誌
	docker logs -f $(IMAGE_NAME)

.PHONY: docker-push
docker-push: ## 推送映像到 Registry
	@echo "$(BLUE)推送映像到 Registry...$(NC)"
	docker push $(REGISTRY)/$(IMAGE_NAME):$(VERSION)
	docker push $(REGISTRY)/$(IMAGE_NAME):latest
	@echo "$(GREEN)映像推送成功$(NC)"

.PHONY: docker-compose-up
docker-compose-up: ## 使用 Docker Compose 啟動
	@echo "$(BLUE)使用 Docker Compose 啟動...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)服務已啟動: http://localhost:8501$(NC)"

.PHONY: docker-compose-down
docker-compose-down: ## 使用 Docker Compose 停止
	docker-compose down

.PHONY: docker-compose-logs
docker-compose-logs: ## 查看 Docker Compose 日誌
	docker-compose logs -f

# ==================== Kubernetes 操作 ====================

.PHONY: k8s-apply
k8s-apply: ## 部署到 Kubernetes
	@echo "$(BLUE)部署到 Kubernetes...$(NC)"
	kubectl apply -f k8s/ -n $(NAMESPACE)
	@echo "$(GREEN)部署成功$(NC)"

.PHONY: k8s-delete
k8s-delete: ## 從 Kubernetes 刪除
	@echo "$(BLUE)從 Kubernetes 刪除...$(NC)"
	kubectl delete -f k8s/ -n $(NAMESPACE)

.PHONY: k8s-status
k8s-status: ## 查看 Kubernetes 部署狀態
	@echo "$(BLUE)Kubernetes 部署狀態:$(NC)"
	kubectl get all -l app=$(IMAGE_NAME) -n $(NAMESPACE)

.PHONY: k8s-logs
k8s-logs: ## 查看 Kubernetes 日誌
	kubectl logs -f -l app=$(IMAGE_NAME) -n $(NAMESPACE) --tail=100

.PHONY: k8s-describe
k8s-describe: ## 查看 Pod 詳細資訊
	kubectl describe pods -l app=$(IMAGE_NAME) -n $(NAMESPACE)

.PHONY: k8s-port-forward
k8s-port-forward: ## 轉發 Kubernetes 服務到本地
	@echo "$(BLUE)轉發服務到本地 8501 端口...$(NC)"
	@echo "$(GREEN)訪問: http://localhost:8501$(NC)"
	kubectl port-forward svc/$(IMAGE_NAME) 8501:80 -n $(NAMESPACE)

.PHONY: k8s-update
k8s-update: docker-build docker-push ## 更新 Kubernetes 部署（重新建立並推送映像）
	@echo "$(BLUE)更新 Kubernetes 部署...$(NC)"
	kubectl set image deployment/$(IMAGE_NAME) $(IMAGE_NAME)=$(REGISTRY)/$(IMAGE_NAME):$(VERSION) -n $(NAMESPACE)
	kubectl rollout status deployment/$(IMAGE_NAME) -n $(NAMESPACE)
	@echo "$(GREEN)更新完成$(NC)"

.PHONY: k8s-rollback
k8s-rollback: ## 回滾 Kubernetes 部署
	@echo "$(BLUE)回滾部署...$(NC)"
	kubectl rollout undo deployment/$(IMAGE_NAME) -n $(NAMESPACE)
	kubectl rollout status deployment/$(IMAGE_NAME) -n $(NAMESPACE)

.PHONY: k8s-scale
k8s-scale: ## 擴展 Pods 數量（使用：make k8s-scale REPLICAS=5）
	@echo "$(BLUE)擴展到 $(REPLICAS) 個副本...$(NC)"
	kubectl scale deployment/$(IMAGE_NAME) --replicas=$(REPLICAS) -n $(NAMESPACE)

.PHONY: k8s-restart
k8s-restart: ## 重啟 Pods
	@echo "$(BLUE)重啟 Pods...$(NC)"
	kubectl rollout restart deployment/$(IMAGE_NAME) -n $(NAMESPACE)

# ==================== 監控和除錯 ====================

.PHONY: k8s-top
k8s-top: ## 查看資源使用情況
	@echo "$(BLUE)Pod 資源使用:$(NC)"
	kubectl top pods -l app=$(IMAGE_NAME) -n $(NAMESPACE)

.PHONY: k8s-events
k8s-events: ## 查看相關事件
	kubectl get events -n $(NAMESPACE) --sort-by='.lastTimestamp' | grep $(IMAGE_NAME)

.PHONY: k8s-hpa-status
k8s-hpa-status: ## 查看 HPA 狀態
	kubectl get hpa $(IMAGE_NAME) -n $(NAMESPACE)

.PHONY: k8s-shell
k8s-shell: ## 進入 Pod Shell
	@POD=$$(kubectl get pods -l app=$(IMAGE_NAME) -n $(NAMESPACE) -o jsonpath='{.items[0].metadata.name}'); \
	echo "$(BLUE)進入 Pod: $$POD$(NC)"; \
	kubectl exec -it $$POD -n $(NAMESPACE) -- /bin/bash

# ==================== 完整流程 ====================

.PHONY: deploy-local
deploy-local: docker-compose-up ## 本地完整部署（Docker Compose）

.PHONY: deploy-k8s
deploy-k8s: docker-build docker-push k8s-apply ## Kubernetes 完整部署
	@echo "$(GREEN)部署完成！$(NC)"
	@echo "運行以下命令訪問應用："
	@echo "  $(YELLOW)make k8s-port-forward$(NC)"

.PHONY: clean
clean: docker-stop docker-compose-down ## 清理本地資源
	@echo "$(BLUE)清理本地資源...$(NC)"
	docker rmi $(IMAGE_NAME):$(VERSION) 2>/dev/null || true
	rm -rf __pycache__ output/*

.PHONY: test
test: ## 運行測試
	@echo "$(YELLOW)測試功能尚未實作$(NC)"

# ==================== 資訊查詢 ====================

.PHONY: info
info: ## 顯示當前配置
	@echo "$(BLUE)當前配置:$(NC)"
	@echo "  Registry: $(REGISTRY)"
	@echo "  Image: $(IMAGE_NAME)"
	@echo "  Version: $(VERSION)"
	@echo "  Namespace: $(NAMESPACE)"
	@echo ""
	@echo "$(BLUE)Docker 映像:$(NC)"
	@docker images | grep $(IMAGE_NAME) || echo "  無本地映像"
	@echo ""
	@echo "$(BLUE)Kubernetes 資源:$(NC)"
	@kubectl get all -l app=$(IMAGE_NAME) -n $(NAMESPACE) 2>/dev/null || echo "  未部署到 Kubernetes"

# 預設目標
.DEFAULT_GOAL := help

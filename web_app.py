#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR Code 轉換程式 - Web 版本
使用 Streamlit 建立互動式網頁介面
"""

import streamlit as st
import cv2
import qrcode
import io
from PIL import Image
import zipfile
from datetime import datetime
import os
from streamlit_paste_button import paste_image_button as pbutton

try:
    from pyzbar.pyzbar import decode
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False

# 初始化 WeChat QRCode 偵測器
WECHAT_DETECTOR = None
WECHAT_AVAILABLE = False

try:
    # 模型檔案路徑
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    detect_prototxt = os.path.join(model_dir, 'detect.prototxt')
    detect_caffemodel = os.path.join(model_dir, 'detect.caffemodel')
    sr_prototxt = os.path.join(model_dir, 'sr.prototxt')
    sr_caffemodel = os.path.join(model_dir, 'sr.caffemodel')
    
    # 檢查檔案是否存在
    if all(os.path.exists(f) for f in [detect_prototxt, detect_caffemodel, sr_prototxt, sr_caffemodel]):
        # WECHAT_DETECTOR = cv2.wechat_qrcode_WeChatQRCode(
        #     detect_prototxt, detect_caffemodel,
        #     sr_prototxt, sr_caffemodel
        # )
        WECHAT_DETECTOR = cv2.wechat_qrcode_WeChatQRCode()

        WECHAT_AVAILABLE = True
except Exception as e:
    print(f"WeChat QRCode 初始化失敗: {e}")
    WECHAT_AVAILABLE = False

# 設定頁面
st.set_page_config(
    page_title="QR Code 轉換器",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂 CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        height: 3rem;
        font-size: 1.1rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)


def read_qrcode_from_image(image):
    """從圖片讀取 QR code - 優化版，優先順序: WeChat QRCode → pyzbar → OpenCV"""
    import numpy as np
    
    # 轉換為 numpy array
    img_array = np.array(image)
    detected_qrcodes = []
    detected_data_set = set()
    
    # 轉換為不同格式備用
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # ========================================
    # 優先級 1: WeChat QRCode（最強！）
    # ========================================
    if WECHAT_AVAILABLE and WECHAT_DETECTOR:
        try:
            # 策略 1.1: 原圖
            results, points = WECHAT_DETECTOR.detectAndDecode(img_bgr)
            for data in results:
                if data and data not in detected_data_set:
                    detected_qrcodes.append(data)
                    detected_data_set.add(data)
            
            # 策略 1.2: 增強對比度
            if len(detected_qrcodes) < 3:
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
                enhanced = clahe.apply(gray)
                enhanced_bgr = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
                results, points = WECHAT_DETECTOR.detectAndDecode(enhanced_bgr)
                for data in results:
                    if data and data not in detected_data_set:
                        detected_qrcodes.append(data)
                        detected_data_set.add(data)
            
            # 策略 1.3: 二值化
            if len(detected_qrcodes) < 3:
                _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                binary_bgr = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
                results, points = WECHAT_DETECTOR.detectAndDecode(binary_bgr)
                for data in results:
                    if data and data not in detected_data_set:
                        detected_qrcodes.append(data)
                        detected_data_set.add(data)
            
            # 如果 WeChat QRCode 找到所有 QR code，直接返回
            if len(detected_qrcodes) >= 3:
                return detected_qrcodes
                
        except Exception as e:
            print(f"WeChat QRCode 偵測錯誤: {e}")
    
    # ========================================
    # 優先級 2: pyzbar（高精度）
    # ========================================
    if PYZBAR_AVAILABLE and len(detected_qrcodes) < 3:
        try:
            # 策略 2.1: 原圖
            decoded_objects = decode(img_array)
            for obj in decoded_objects:
                if obj.type == 'QRCODE':
                    data = obj.data.decode('utf-8')
                    if data and data not in detected_data_set:
                        detected_qrcodes.append(data)
                        detected_data_set.add(data)
            
            # 策略 2.2: 灰階
            if len(detected_qrcodes) < 3:
                decoded_objects = decode(gray)
                for obj in decoded_objects:
                    if obj.type == 'QRCODE':
                        data = obj.data.decode('utf-8')
                        if data and data not in detected_data_set:
                            detected_qrcodes.append(data)
                            detected_data_set.add(data)
            
            # 策略 2.3: 增強對比度
            if len(detected_qrcodes) < 3:
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                enhanced = clahe.apply(gray)
                decoded_objects = decode(enhanced)
                for obj in decoded_objects:
                    if obj.type == 'QRCODE':
                        data = obj.data.decode('utf-8')
                        if data and data not in detected_data_set:
                            detected_qrcodes.append(data)
                            detected_data_set.add(data)
            
            # 策略 2.4: 二值化
            if len(detected_qrcodes) < 3:
                _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                decoded_objects = decode(binary)
                for obj in decoded_objects:
                    if obj.type == 'QRCODE':
                        data = obj.data.decode('utf-8')
                        if data and data not in detected_data_set:
                            detected_qrcodes.append(data)
                            detected_data_set.add(data)
            
            # 如果 pyzbar 找到所有 QR code，直接返回
            if len(detected_qrcodes) >= 3:
                return detected_qrcodes
                
        except Exception as e:
            print(f"pyzbar 偵測錯誤: {e}")
    
    # ========================================
    # 優先級 3: OpenCV（標準精度，最後備用）
    # ========================================
    if len(detected_qrcodes) < 3:
        try:
            detector = cv2.QRCodeDetector()
            
            # 策略 3.1: 原圖
            success, decoded_info, points, _ = detector.detectAndDecodeMulti(img_bgr)
            if success and decoded_info:
                for data in decoded_info:
                    if data and data not in detected_data_set:
                        detected_qrcodes.append(data)
                        detected_data_set.add(data)
            
            # 策略 3.2: 增強對比度
            if len(detected_qrcodes) < 3:
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
                enhanced = clahe.apply(gray)
                enhanced_bgr = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
                success, decoded_info, points, _ = detector.detectAndDecodeMulti(enhanced_bgr)
                if success and decoded_info:
                    for data in decoded_info:
                        if data and data not in detected_data_set:
                            detected_qrcodes.append(data)
                            detected_data_set.add(data)
            
            # 策略 3.3: 二值化
            if len(detected_qrcodes) < 3:
                _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                binary_bgr = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
                success, decoded_info, points, _ = detector.detectAndDecodeMulti(binary_bgr)
                if success and decoded_info:
                    for data in decoded_info:
                        if data and data not in detected_data_set:
                            detected_qrcodes.append(data)
                            detected_data_set.add(data)
            
            # 策略 3.4: 反轉顏色（處理深色背景）
            if len(detected_qrcodes) < 3:
                inverted = cv2.bitwise_not(gray)
                inverted_bgr = cv2.cvtColor(inverted, cv2.COLOR_GRAY2BGR)
                success, decoded_info, points, _ = detector.detectAndDecodeMulti(inverted_bgr)
                if success and decoded_info:
                    for data in decoded_info:
                        if data and data not in detected_data_set:
                            detected_qrcodes.append(data)
                            detected_data_set.add(data)
            
            # 策略 3.5: 調整亮度
            if len(detected_qrcodes) < 3:
                brightened = cv2.convertScaleAbs(gray, alpha=1.5, beta=30)
                brightened_bgr = cv2.cvtColor(brightened, cv2.COLOR_GRAY2BGR)
                success, decoded_info, points, _ = detector.detectAndDecodeMulti(brightened_bgr)
                if success and decoded_info:
                    for data in decoded_info:
                        if data and data not in detected_data_set:
                            detected_qrcodes.append(data)
                            detected_data_set.add(data)
                            
        except Exception as e:
            print(f"OpenCV 偵測錯誤: {e}")
    
    return detected_qrcodes


def convert_content(content):
    """轉換內容"""
    return content.replace("[CVS]", "[MyCard]")


def generate_qrcode(content):
    """生成 QR code"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def process_image(uploaded_file):
    """處理單個圖片"""
    image = Image.open(uploaded_file)
    
    # 讀取 QR code
    contents = read_qrcode_from_image(image)
    
    if not contents:
        return None, image, "無法偵測到 QR code"
    
    # 轉換並生成新的 QR code
    results = []
    for idx, content in enumerate(contents, 1):
        converted = convert_content(content)
        new_qr = generate_qrcode(converted)
        results.append({
            'index': idx,
            'original': content,
            'converted': converted,
            'qr_image': new_qr
        })
    
    return results, image, None


def main():
    """主程式"""
    
    # 標題
    st.title("🔄 QR Code 轉換器")
    st.markdown("### 將 [CVS] 轉換為 [MyCard]")
    
    # 側邊欄
    with st.sidebar:
        st.header("ℹ️ 使用說明")
        st.markdown("""
        1. 上傳或貼上包含 QR code 的圖片
        2. 系統自動偵測並轉換
        3. 下載轉換後的 QR code
        
        **輸入方式**
        - 📁 上傳檔案
        - 📋 從剪貼簿貼上（Ctrl+V / Cmd+V）
        - 📸 截圖後直接貼上
        
        **支援格式**
        - PNG, JPG, JPEG
        - BMP, GIF, TIFF
        
        **功能特色**
        - ✅ 自動偵測多個 QR code
        - ✅ 批次處理多張圖片
        - ✅ 即時預覽結果
        - ✅ 一鍵下載所有結果
        - ✨ 支援剪貼簿貼上
        """)
        
        st.divider()
        
        st.header("⚙️ 偵測器狀態")
        st.markdown("**偵測優先順序**")
        
        # WeChat QRCode 狀態
        if WECHAT_AVAILABLE:
            st.success("🥇 WeChat QRCode（超高精度）")
        else:
            st.error("❌ WeChat QRCode 未啟用")
        
        # pyzbar 狀態
        if PYZBAR_AVAILABLE:
            st.success("🥈 pyzbar（高精度）")
        else:
            st.warning("⚠️ pyzbar 不可用")
        
        # OpenCV 狀態
        st.info("🥉 OpenCV QRCodeDetector（標準精度）")
        
        st.markdown("---")
        st.caption("""
        **偵測策略**
        - 優先使用 WeChat QRCode（微信團隊優化）
        - 備用 pyzbar（高容錯率）
        - 最後使用 OpenCV（穩定可靠）
        """)
        
        st.info("""
        💡 **提示**
        
        為獲得最佳偵測效果：
        - 確保 QR code 清晰可見
        - 避免圖片過度壓縮
        - 建議圖片解析度 ≥ 1000px
        """)
    
    # 主要內容區域
    tab1, tab2 = st.tabs(["📤 單張上傳", "📦 批次上傳"])
    
    with tab1:
        st.header("上傳或貼上圖片")
        
        # 建立兩個選項：上傳檔案或從剪貼簿貼上
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📁 上傳檔案")
            uploaded_file = st.file_uploader(
                "選擇包含 QR code 的圖片",
                type=['png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff'],
                key="single"
            )
        
        with col2:
            st.subheader("📋 從剪貼簿貼上")
            paste_result = pbutton(
                label="📋 點擊貼上圖片",
                errors="raise",
                key="paste_button"
            )
        
        # 處理上傳或貼上的圖片
        image_to_process = None
        image_source = None
        
        if uploaded_file:
            image_to_process = uploaded_file
            image_source = "uploaded"
        elif paste_result.image_data is not None:
            # 將貼上的圖片轉換為 BytesIO 對象
            image_to_process = io.BytesIO()
            paste_result.image_data.save(image_to_process, format='PNG')
            image_to_process.seek(0)
            image_source = "pasted"
        
        if image_to_process:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📸 原始圖片")
                image = Image.open(image_to_process)
                st.image(image, use_container_width=True)
                
                if image_source == "pasted":
                    st.info("✨ 圖片來自剪貼簿")
                else:
                    st.info(f"📁 檔案: {uploaded_file.name}")
            
            with st.spinner("🔍 正在偵測和轉換 QR code..."):
                # 重置檔案指針
                if image_source == "uploaded":
                    uploaded_file.seek(0)
                else:
                    image_to_process.seek(0)
                results, original_image, error = process_image(image_to_process)
            
            if error:
                st.error(f"❌ {error}")
            elif results:
                with col2:
                    st.subheader("📊 處理結果")
                    st.success(f"✅ 偵測到 {len(results)} 個 QR code")
                
                # 顯示每個結果
                for result in results:
                    with st.expander(f"QR Code #{result['index']}", expanded=True):
                        st.markdown(f"**原始內容：** `{result['original']}`")
                        st.markdown(f"**轉換內容：** `{result['converted']}`")
                        
                        if result['original'] != result['converted']:
                            st.success("✅ 已轉換")
                        else:
                            st.warning("⚠️ 內容未變更（未包含 [CVS]）")
                        
                        # 轉換 PIL Image 為 bytes 以便顯示
                        img_bytes = io.BytesIO()
                        result['qr_image'].save(img_bytes, format='PNG')
                        img_bytes.seek(0)
                        
                        # 顯示 QR code
                        st.image(img_bytes, width=250)
                        
                        # 重置 BytesIO 以便下載
                        img_bytes.seek(0)
                        
                        st.download_button(
                            label=f"⬇️ 下載 QR Code #{result['index']}",
                            data=img_bytes,
                            file_name=f"qrcode_{result['index']}.png",
                            mime="image/png",
                            key=f"download_{result['index']}"
                        )
    
    with tab2:
        st.header("批次上傳多張圖片")
        uploaded_files = st.file_uploader(
            "選擇多張包含 QR code 的圖片",
            type=['png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff'],
            accept_multiple_files=True,
            key="multiple"
        )
        
        if uploaded_files:
            st.info(f"📁 已上傳 {len(uploaded_files)} 張圖片")
            
            if st.button("🚀 開始批次處理", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                all_results = []
                incomplete_files = []
                
                for idx, file in enumerate(uploaded_files):
                    status_text.text(f"處理中: {file.name} ({idx + 1}/{len(uploaded_files)})")
                    
                    results, _, error = process_image(file)
                    
                    if error:
                        incomplete_files.append((file.name, 0, error))
                    elif results:
                        all_results.append({
                            'filename': file.name,
                            'results': results
                        })
                        if len(results) != 3:
                            incomplete_files.append((file.name, len(results), None))
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                status_text.empty()
                progress_bar.empty()
                
                # 顯示統計
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("總圖片數", len(uploaded_files))
                with col2:
                    st.metric("成功處理", len(all_results))
                with col3:
                    total_qrcodes = sum(len(r['results']) for r in all_results)
                    st.metric("總 QR code", total_qrcodes)
                
                # 顯示不完整檔案
                if incomplete_files:
                    st.warning(f"⚠️ {len(incomplete_files)} 個檔案偵測不完整")
                    with st.expander("查看詳情"):
                        for filename, count, error in incomplete_files:
                            if error:
                                st.text(f"❌ {filename}: {error}")
                            else:
                                st.text(f"⚠️ {filename}: 偵測到 {count} 個 QR code（預期 3 個）")
                else:
                    st.success("✅ 所有檔案都成功處理！")
                
                # 建立 ZIP 下載
                if all_results:
                    st.divider()
                    st.subheader("📦 下載所有結果")
                    
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for file_result in all_results:
                            for qr_result in file_result['results']:
                                img_bytes = io.BytesIO()
                                qr_result['qr_image'].save(img_bytes, format='PNG')
                                img_bytes.seek(0)
                                
                                if len(file_result['results']) == 1:
                                    filename = f"{file_result['filename'].rsplit('.', 1)[0]}.png"
                                else:
                                    filename = f"{file_result['filename'].rsplit('.', 1)[0]}_{qr_result['index']}.png"
                                
                                zip_file.writestr(filename, img_bytes.getvalue())
                    
                    zip_buffer.seek(0)
                    
                    st.download_button(
                        label="⬇️ 下載所有 QR Code (ZIP)",
                        data=zip_buffer,
                        file_name=f"qrcodes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                        mime="application/zip"
                    )
                
                # 顯示詳細結果
                with st.expander("📋 查看詳細結果"):
                    for file_result in all_results:
                        st.markdown(f"### {file_result['filename']}")
                        for qr_result in file_result['results']:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.text(f"QR #{qr_result['index']}: {qr_result['original']} → {qr_result['converted']}")
                            with col2:
                                # 轉換 PIL Image 為 bytes 以便顯示
                                img_preview = io.BytesIO()
                                qr_result['qr_image'].save(img_preview, format='PNG')
                                img_preview.seek(0)
                                st.image(img_preview, width=100)
    
    # 頁尾
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>QR Code 轉換器 v1.0 | 支援多平台使用</p>
        <p>💻 桌面版 | 🌐 網頁版 | 📱 行動版</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

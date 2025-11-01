#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR Code 轉換程式
讀取 input 資料夾中的 QR code 圖片，將內容從 [CVS] 轉換為 [MyCard]，
然後生成新的 QR code 儲存到 output 資料夾
"""

import os
import cv2
import qrcode
import shutil
from pathlib import Path
try:
    from pyzbar.pyzbar import decode
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False
    print("⚠️  pyzbar 未安裝，將使用 OpenCV 偵測器（可能較不準確）")
    print("   建議安裝: pip3 install pyzbar")


class QRCodeConverter:
    """QR Code 轉換器類別"""
    
    def __init__(self, input_folder: str = "input", output_folder: str = "output"):
        """
        初始化轉換器
        
        Args:
            input_folder: 輸入資料夾路徑
            output_folder: 輸出資料夾路徑
        """
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        
        # 清空輸出資料夾
        self._clear_output_folder()
        
        # 確保輸出資料夾存在
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        # 支援的圖片格式
        self.supported_formats = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'}
    
    def _clear_output_folder(self):
        """清空輸出資料夾"""
        if self.output_folder.exists():
            try:
                # 刪除資料夾中的所有檔案
                for item in self.output_folder.iterdir():
                    if item.is_file():
                        item.unlink()
                        print(f"  🗑️  已刪除: {item.name}")
                    elif item.is_dir():
                        shutil.rmtree(item)
                        print(f"  🗑️  已刪除資料夾: {item.name}")
                
                if any(self.output_folder.iterdir()):
                    print("  ✅ 輸出資料夾已清空")
            except Exception as e:
                print(f"  ⚠️  清空輸出資料夾時發生錯誤: {e}")
    
    def read_qrcode(self, image_path: Path) -> list[str]:
        """
        讀取 QR code 圖片並解碼內容（支援多個 QR code）
        
        Args:
            image_path: 圖片檔案路徑
            
        Returns:
            解碼後的文字內容列表，如果失敗則返回空列表
        """
        try:
            # 讀取圖片
            image = cv2.imread(str(image_path))
            if image is None:
                print(f"❌ 無法讀取圖片: {image_path}")
                return []
            
            detected_qrcodes = []
            detected_data_set = set()  # 用於去重
            
            print(f"  📐 圖片尺寸: {image.shape[1]}x{image.shape[0]}")
            
            # 方法 1: 使用 pyzbar 在原圖上偵測（更準確）
            if PYZBAR_AVAILABLE:
                decoded_objects = decode(image)
                print(f"  🔍 pyzbar 在原圖偵測到 {len(decoded_objects)} 個條碼")
                for obj in decoded_objects:
                    if obj.type == 'QRCODE':
                        data = obj.data.decode('utf-8')
                        if data and data not in detected_data_set:
                            detected_qrcodes.append(data)
                            detected_data_set.add(data)
                            print(f"     → QR code: {data[:50]}...")
            
            # 方法 2: 轉灰階後用 pyzbar 再試一次
            if PYZBAR_AVAILABLE:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                decoded_objects = decode(gray)
                print(f"  🔍 pyzbar 在灰階圖偵測到 {len(decoded_objects)} 個條碼")
                for obj in decoded_objects:
                    if obj.type == 'QRCODE':
                        data = obj.data.decode('utf-8')
                        if data and data not in detected_data_set:
                            detected_qrcodes.append(data)
                            detected_data_set.add(data)
                            print(f"     → QR code: {data[:50]}...")
            
            # 方法 3: 提高對比度後再試
            if PYZBAR_AVAILABLE:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # 使用 CLAHE (對比度限制自適應直方圖均衡化)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                enhanced = clahe.apply(gray)
                decoded_objects = decode(enhanced)
                print(f"  🔍 pyzbar 在增強對比度圖偵測到 {len(decoded_objects)} 個條碼")
                for obj in decoded_objects:
                    if obj.type == 'QRCODE':
                        data = obj.data.decode('utf-8')
                        if data and data not in detected_data_set:
                            detected_qrcodes.append(data)
                            detected_data_set.add(data)
                            print(f"     → QR code: {data[:50]}...")
            
            # 方法 4: 使用 OpenCV 的 detectAndDecodeMulti
            detector = cv2.QRCodeDetector()
            success, decoded_info, points, _ = detector.detectAndDecodeMulti(image)
            
            if success and decoded_info:
                print(f"  🔍 OpenCV Multi 偵測到 {len(decoded_info)} 個 QR code")
                for data in decoded_info:
                    if data and data not in detected_data_set:
                        detected_qrcodes.append(data)
                        detected_data_set.add(data)
                        print(f"     → QR code: {data[:50]}...")
            
            # 方法 5: 二值化後用 pyzbar
            if PYZBAR_AVAILABLE:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                decoded_objects = decode(binary)
                print(f"  🔍 pyzbar 在二值化圖偵測到 {len(decoded_objects)} 個條碼")
                for obj in decoded_objects:
                    if obj.type == 'QRCODE':
                        data = obj.data.decode('utf-8')
                        if data and data not in detected_data_set:
                            detected_qrcodes.append(data)
                            detected_data_set.add(data)
                            print(f"     → QR code: {data[:50]}...")
            
            if detected_qrcodes:
                print(f"  ✅ 總共成功偵測到 {len(detected_qrcodes)} 個不重複的 QR code")
                return detected_qrcodes
            
            print(f"  ⚠️  嘗試所有方法後仍無法偵測到 QR code")
            return []
                
        except Exception as e:
            print(f"❌ 讀取 QR code 時發生錯誤 ({image_path}): {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def convert_content(self, content: str) -> str:
        """
        將內容從 [CVS] 轉換為 [MyCard]
        
        Args:
            content: 原始內容
            
        Returns:
            轉換後的內容
        """
        # 替換 [CVS] 為 [MyCard]
        converted = content.replace("[CVS]", "[MyCard]")
        return converted
    
    def generate_qrcode(self, content: str, output_path: Path) -> bool:
        """
        生成新的 QR code 圖片
        
        Args:
            content: QR code 內容
            output_path: 輸出檔案路徑
            
        Returns:
            是否成功生成
        """
        try:
            # 建立 QR code 物件
            qr = qrcode.QRCode(
                version=1,  # 控制 QR code 的大小 (1-40)
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高容錯率
                box_size=10,  # 每個格子的像素大小
                border=4,  # 邊框寬度
            )
            
            # 添加資料
            qr.add_data(content)
            qr.make(fit=True)
            
            # 建立圖片
            img = qr.make_image(fill_color="black", back_color="white")
            
            # 儲存圖片
            img.save(str(output_path))
            
            return True
            
        except Exception as e:
            print(f"❌ 生成 QR code 時發生錯誤 ({output_path}): {e}")
            return False
    
    def process_single_file(self, image_path: Path) -> int:
        """
        處理單一圖片檔案（支援多個 QR code）
        
        Args:
            image_path: 圖片檔案路徑
            
        Returns:
            成功偵測到的 QR code 數量，失敗返回 0
        """
        print(f"\n處理中: {image_path.name}")
        
        # 讀取 QR code（可能有多個）
        contents = self.read_qrcode(image_path)
        if not contents:
            return 0
        
        print(f"  偵測到 {len(contents)} 個 QR code")
        
        # 處理每個 QR code
        success = True
        for idx, content in enumerate(contents, 1):
            print(f"\n  QR code #{idx}:")
            print(f"    原始內容: {content}")
            
            # 轉換內容
            converted_content = self.convert_content(content)
            print(f"    轉換內容: {converted_content}")
            
            # 檢查是否有變更
            if content == converted_content:
                print(f"    ⚠️  內容沒有變更（未包含 [CVS]）")
            
            # 生成輸出檔案名稱
            # 如果只有一個 QR code，使用原始檔名
            # 如果有多個，加上序號：filename_1.png, filename_2.png
            if len(contents) == 1:
                output_filename = image_path.name
            else:
                stem = image_path.stem  # 檔名（不含副檔名）
                suffix = image_path.suffix  # 副檔名
                output_filename = f"{stem}_{idx}{suffix}"
            
            output_path = self.output_folder / output_filename
            
            # 生成新的 QR code
            if self.generate_qrcode(converted_content, output_path):
                print(f"    ✅ 成功儲存到: {output_filename}")
            else:
                success = False
        
        return len(contents) if success else 0
    
    def process_all(self) -> tuple[int, int, list]:
        """
        處理所有圖片檔案
        
        Returns:
            (成功數量, 失敗數量, 不完整檔案列表) 的元組
        """
        # 檢查輸入資料夾是否存在
        if not self.input_folder.exists():
            print(f"❌ 輸入資料夾不存在: {self.input_folder}")
            return 0, 0, []
        
        # 取得所有圖片檔案
        image_files = [
            f for f in self.input_folder.iterdir()
            if f.is_file() and f.suffix.lower() in self.supported_formats
        ]
        
        if not image_files:
            print(f"⚠️  在 {self.input_folder} 中找不到任何圖片檔案")
            return 0, 0, []
        
        print(f"找到 {len(image_files)} 個圖片檔案")
        print("=" * 60)
        
        # 處理每個檔案
        success_count = 0
        fail_count = 0
        incomplete_files = []  # 記錄沒有偵測到 3 個 QR code 的檔案
        
        for image_file in image_files:
            qr_count = self.process_single_file(image_file)
            if qr_count > 0:
                success_count += 1
                # 如果偵測到的 QR code 數量不是 3 個，記錄下來
                if qr_count != 3:
                    incomplete_files.append((image_file.name, qr_count))
            else:
                fail_count += 1
        
        return success_count, fail_count, incomplete_files


def main():
    """主程式"""
    print("QR Code 轉換程式")
    print("將 [CVS] 轉換為 [MyCard]")
    print("=" * 60)
    
    # 建立轉換器
    converter = QRCodeConverter(input_folder="input", output_folder="output")
    
    # 處理所有檔案
    success, fail, incomplete_files = converter.process_all()
    
    # 顯示結果
    print("\n" + "=" * 60)
    print(f"處理完成！")
    print(f"✅ 成功: {success} 個")
    print(f"❌ 失敗: {fail} 個")
    
    # 顯示並寫入沒有偵測到 3 個 QR code 的檔案
    if incomplete_files:
        print("\n" + "=" * 60)
        print("⚠️  以下檔案沒有偵測到 3 個 QR code：")
        
        # 寫入報告檔案
        report_path = Path("incomplete_files_report.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("QR Code 偵測不完整報告\n")
            f.write("=" * 60 + "\n")
            f.write(f"生成時間: {Path.cwd()}\n\n")
            f.write(f"總共處理: {success + fail} 個檔案\n")
            f.write(f"成功: {success} 個\n")
            f.write(f"失敗: {fail} 個\n")
            f.write(f"偵測不完整: {len(incomplete_files)} 個\n\n")
            f.write("=" * 60 + "\n")
            f.write("偵測不完整的檔案列表：\n\n")
            
            for filename, count in incomplete_files:
                msg = f"   • {filename}: 偵測到 {count} 個 QR code"
                print(msg)
                f.write(f"{filename}\n")
                f.write(f"  偵測到: {count} 個 QR code\n")
                f.write(f"  缺少: {3 - count} 個 QR code\n\n")
        
        print(f"\n📄 報告已儲存到: {report_path.absolute()}")
    else:
        print("\n✅ 所有檔案都成功偵測到 3 個 QR code！")
        # 如果所有檔案都完整，刪除舊的報告檔案（如果存在）
        report_path = Path("incomplete_files_report.txt")
        if report_path.exists():
            report_path.unlink()
            print("📄 已刪除舊的報告檔案")
    
    print(f"\n輸出資料夾: {converter.output_folder.absolute()}")


if __name__ == "__main__":
    main()

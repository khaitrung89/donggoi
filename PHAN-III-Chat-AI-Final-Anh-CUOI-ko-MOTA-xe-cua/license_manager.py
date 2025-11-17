import hashlib
import json
import os
from pathlib import Path
from typing import Optional

LICENSE_FILE = "license.dat"
LICENSE_KEY_FORMAT = "XXXX-XXXX-XXXX-XXXX"

# Danh sách key mẫu (có thể mở rộng)
VALID_LICENSE_KEYS = [
    "ABCD-EFGH-IJKL-MNOP",
    "1234-5678-9012-3456", 
    "TEST-KEYS-2024-DEMO",
    "PROD-UCTI-ONKE-Y2024"
]

def validate_key_format(key: str) -> bool:
    """Kiểm tra định dạng key: XXXX-XXXX-XXXX-XXXX"""
    parts = key.split("-")
    if len(parts) != 4:
        return False
    
    for part in parts:
        if len(part) != 4 or not part.isalnum():
            return False
    
    return True

def validate_key_offline(key: str) -> bool:
    """Kiểm tra key offline đơn giản bằng checksum"""
    if not validate_key_format(key):
        return False
    
    # Tính checksum từ key
    key_hash = hashlib.md5(key.encode()).hexdigest()
    
    # Kiểm tra xem key có trong danh sách hợp lệ không
    return key in VALID_LICENSE_KEYS

def validate_key_online(key: str) -> bool:
    """Kiểm tra key online (giả lập) - có thể mở rộng thành API thực tế"""
    # Giả lập API check online
    # Trong thực tế, bạn sẽ gọi API thực để kiểm tra
    if not validate_key_format(key):
        return False
    
    # Giả lập response từ server
    # Trả về True nếu key hợp lệ
    return key in VALID_LICENSE_KEYS

def save_license(key: str) -> bool:
    """Lưu key vào file license.dat ẩn"""
    try:
        license_data = {
            "key": key,
            "validated": True,
            "checksum": hashlib.md5(key.encode()).hexdigest()
        }
        
        # Tạo file ẩn license.dat
        license_path = Path(LICENSE_FILE)
        with license_path.open("w", encoding="utf-8") as f:
            json.dump(license_data, f, indent=2)
        
        # Ẩn file trên Windows (nếu có thể)
        if os.name == 'nt':
            try:
                os.system(f'attrib +h "{LICENSE_FILE}"')
            except:
                pass
        
        return True
    except Exception as e:
        print(f"Lỗi khi lưu license: {e}")
        return False

def load_license() -> Optional[str]:
    """Đọc key từ file license.dat"""
    try:
        license_path = Path(LICENSE_FILE)
        if not license_path.exists():
            return None
        
        with license_path.open("r", encoding="utf-8") as f:
            license_data = json.load(f)
        
        key = license_data.get("key")
        validated = license_data.get("validated", False)
        checksum = license_data.get("checksum")
        
        # Kiểm tra checksum
        if key and validated and checksum:
            expected_checksum = hashlib.md5(key.encode()).hexdigest()
            if checksum == expected_checksum:
                return key
        
        return None
    except Exception as e:
        print(f"Lỗi khi đọc license: {e}")
        return None

def check_license() -> bool:
    """Kiểm tra license đã được kích hoạt chưa"""
    # Thử đọc license từ file
    saved_key = load_license()
    if saved_key:
        # Kiểm tra lại key đã lưu
        return validate_key_offline(saved_key)
    
    return False

def request_license() -> bool:
    """Yêu cầu người dùng nhập license key"""
    print("=" * 50)
    print("🔐 YÊU CẦU KÍCH HOẠT BẢN QUYỀN")
    print("=" * 50)
    print(f"Vui lòng nhập key bản quyền theo định dạng: {LICENSE_KEY_FORMAT}")
    print("Lưu ý: Key phải gồm 4 nhóm, mỗi nhóm 4 ký tự, cách nhau bằng dấu gạch ngang")
    print("=" * 50)
    
    max_attempts = 3
    for attempt in range(max_attempts):
        key = input(f"Nhập key bản quyền (lần {attempt + 1}/{max_attempts}): ").strip().upper()
        
        if not key:
            print("❌ Key không được để trống!")
            continue
        
        # Kiểm tra định dạng
        if not validate_key_format(key):
            print(f"❌ Sai định dạng! Key phải theo mẫu: {LICENSE_KEY_FORMAT}")
            continue
        
        # Kiểm tra key
        if validate_key_offline(key):
            if save_license(key):
                print("✅ Key bản quyền hợp lệ!")
                print("✅ Đã kích hoạt bản quyền thành công!")
                return True
            else:
                print("❌ Lỗi khi lưu license!")
                return False
        else:
            print("❌ Key bản quyền không hợp lệ!")
            remaining = max_attempts - attempt - 1
            if remaining > 0:
                print(f"⚠️ Bạn còn {remaining} lần thử!")
    
    print("❌ Đã hết số lần thử! Vui lòng liên hệ để được cấp key bản quyền.")
    return False

def main():
    """Hàm test license manager"""
    print("Kiểm tra license...")
    
    if check_license():
        print("✅ License đã được kích hoạt!")
        return True
    else:
        print("⚠️ Chưa có license hoặc license không hợp lệ!")
        return request_license()

if __name__ == "__main__":
    main()
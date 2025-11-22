# my_license.py
import hashlib

# 🔥 Đổi chuỗi này thành secret riêng của bạn
MASTER_SECRET = "LAM_SIEU_PROMPT_V1_2025"

def normalize_key(key: str) -> str:
    return key.strip().upper().replace("-", "")

def generate_license(email: str) -> str:
    """
    Tạo license key từ email để cấp cho user.
    """
    base = (email.strip().lower() + MASTER_SECRET).encode("utf-8")
    h = hashlib.sha256(base).hexdigest().upper()

    raw = h[:16]  # lấy 16 ký tự đầu
    return "-".join([raw[i:i+4] for i in range(0, 16, 4)])

def verify_license(email: str, license_key: str) -> bool:
    """
    Dùng trong main.py để kiểm tra key user nhập.
    """
    expected = generate_license(email)
    return normalize_key(license_key) == normalize_key(expected)

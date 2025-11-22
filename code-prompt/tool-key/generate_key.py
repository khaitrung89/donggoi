# generate_key.py
import hashlib

# 🔥 Phải giống y MASTER_SECRET trong my_license.py
MASTER_SECRET = "LAM_SIEU_PROMPT_V1_2025"

def normalize_email(email: str) -> str:
    return email.strip().lower()

def generate_license(email: str) -> str:
    base = (normalize_email(email) + MASTER_SECRET).encode("utf-8")
    h = hashlib.sha256(base).hexdigest().upper()

    raw = h[:16]  # lấy 16 ký tự đầu
    return "-".join([raw[i:i+4] for i in range(0, 16, 4)])

if __name__ == "__main__":
    print("====== License Key Generator ======")
    email = input("Nhập email cần tạo key: ").strip()

    if not email:
        print("❌ Email trống!")
        exit()

    key = generate_license(email)
    print("\n✅ License Key:")
    print(key)
    print("\nCopy key này để kích hoạt phần mềm.")

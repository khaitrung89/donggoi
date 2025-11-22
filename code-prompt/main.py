# main.py
from my_license import verify_license  # dùng hàm verify_license trong my_license.py

def main():
    print("===== SIÊU PROMPT TOOL – BẢN CÓ BẢN QUYỀN =====")
    user_email = input("Nhập email đã đăng ký: ").strip()
    user_key = input("Nhập License Key: ").strip()

    if not verify_license(user_email, user_key):
        print("\n❌ License không hợp lệ. Vui lòng kiểm tra lại email hoặc key.")
        print("Nếu bạn chưa mua bản quyền, hãy liên hệ admin để được cấp key.")
        input("Nhấn Enter để thoát...")
        return

    print("\n✅ License hợp lệ. Đang khởi động giao diện...\n")

    # Chỉ import GUI sau khi license OK
    try:
        from gui_app import main as gui_main
    except ImportError as e:
        print(f"❌ Không thể import gui_app: {e}")
        input("Nhấn Enter để thoát...")
        return

    # Chạy GUI Tkinter
    gui_main()


if __name__ == "__main__":
    main()

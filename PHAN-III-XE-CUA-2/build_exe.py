#!/usr/bin/env python
"""
Script để đóng gói FilmAI Prompt Generator thành file .exe
"""

import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Cài đặt PyInstaller nếu chưa có"""
    try:
        import PyInstaller
        print("✅ PyInstaller đã được cài đặt")
        return True
    except ImportError:
        print("📦 Đang cài đặt PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller đã được cài đặt thành công")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi khi cài đặt PyInstaller: {e}")
            return False

def build_executable():
    """Đóng gói thành file .exe"""
    print("🚀 Bắt đầu đóng gói ứng dụng...")
    print("=" * 50)
    
    # Cài đặt PyInstaller
    if not install_pyinstaller():
        return False
    
    # Kiểm tra file spec
    spec_file = Path("build.spec")
    if not spec_file.exists():
        print("❌ Không tìm thấy file build.spec")
        return False
    
    # Chạy PyInstaller với file spec
    try:
        print("🏗️  Đang build với PyInstaller...")
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller", 
            "--clean",  # Xóa cache trước khi build
            "--noconfirm",  # Không hỏi xác nhận
            "build.spec"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build thành công!")
            print("📁 File .exe được tạo trong thư mục: dist/FilmAI-PromptGenerator.exe")
            return True
        else:
            print(f"❌ Lỗi khi build:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi chạy PyInstaller: {e}")
        return False

def main():
    """Hàm chính"""
    print("🎬 FilmAI Prompt Generator - Build Tool")
    print("=" * 50)
    
    # Kiểm tra Python version
    if sys.version_info < (3, 7):
        print("❌ Yêu cầu Python 3.7 trở lên")
        return
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print("=" * 50)
    
    # Build executable
    if build_executable():
        print("\n🎉 Build hoàn tất!")
        print("💡 Bạn có thể tìm file .exe trong thư mục 'dist/'")
        print("💡 Chạy file 'dist/FilmAI-PromptGenerator.exe' để sử dụng tool")
    else:
        print("\n❌ Build thất bại!")
        print("💡 Kiểm tra lỗi ở trên và thử lại")

if __name__ == "__main__":
    main()
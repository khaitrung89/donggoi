@echo off
REM ====================================
REM FilmAI v2.0 Enhanced - Build Script
REM Chay file nay tren Windows de build .exe
REM ====================================

echo.
echo ========================================
echo   FilmAI v2.0 Enhanced - Build Tool
echo ========================================
echo.

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat!
    echo Vui long cai Python tu: https://www.python.org/downloads/
    echo Nho tick "Add Python to PATH" khi cai dat!
    pause
    exit /b 1
)

echo [OK] Python version:
python --version
echo.

REM Kiem tra pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip khong kha dung!
    pause
    exit /b 1
)

echo [OK] pip version:
pip --version
echo.

REM Cai dat dependencies
echo ========================================
echo   Buoc 1: Cai dat dependencies
echo ========================================
echo.
echo Dang cai dat google-generativeai...
pip install google-generativeai --quiet
echo.

echo Dang cai dat PyInstaller...
pip install pyinstaller --quiet
echo.

REM Kiem tra build_enhanced.spec
if not exist "build_enhanced.spec" (
    echo [ERROR] Khong tim thay file build_enhanced.spec!
    pause
    exit /b 1
)

REM Clean build cache
echo ========================================
echo   Buoc 2: Clean build cache
echo ========================================
echo.
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "__pycache__" rmdir /s /q __pycache__
echo [OK] Da xoa cache cu
echo.

REM Build .exe
echo ========================================
echo   Buoc 3: Build file .exe v2.0
echo ========================================
echo.
echo Dang build Enhanced Version...
echo Vui long doi (2-5 phut)
echo.
pyinstaller --clean --noconfirm build_enhanced.spec

if errorlevel 1 (
    echo.
    echo [ERROR] Build that bai!
    echo Vui long kiem tra log o tren.
    pause
    exit /b 1
)

REM Kiem tra ket qua
if exist "dist\FilmAI-PromptGenerator-v2.exe" (
    echo.
    echo ========================================
    echo   BUILD THANH CONG v2.0!
    echo ========================================
    echo.
    echo File .exe da duoc tao tai:
    echo   dist\FilmAI-PromptGenerator-v2.exe
    echo.
    echo Kich thuoc:
    dir "dist\FilmAI-PromptGenerator-v2.exe" | find "FilmAI-PromptGenerator-v2.exe"
    echo.
    echo ========================================
    echo   TINH NANG MOI v2.0:
    echo ========================================
    echo 1. Settings Dialog voi 3 tabs
    echo 2. Quan ly API Keys qua GUI
    echo 3. Chon World Type va AI Model
    echo 4. Tu dong dich Tieng Viet
    echo 5. Chon thu muc Output tuy y
    echo 6. Luu settings vao config.json
    echo.
    echo ========================================
    echo   CACH SU DUNG:
    echo ========================================
    echo 1. Mo thu muc dist\
    echo 2. Chay file FilmAI-PromptGenerator-v2.exe
    echo 3. Nhap license key khi duoc yeu cau
    echo 4. Click nut "Settings" de cau hinh
    echo 5. Paste API keys vao Settings
    echo 6. Chon file scenes.txt va Generate!
    echo.
    echo License keys mau:
    echo   - ABCD-EFGH-IJKL-MNOP
    echo   - 1234-5678-9012-3456
    echo   - TEST-KEYS-2024-DEMO
    echo.
    echo Doc them: README_V2.md
    echo.
    pause
) else (
    echo.
    echo [ERROR] Khong tim thay file .exe sau khi build!
    echo Vui long kiem tra log o tren.
    pause
    exit /b 1
)

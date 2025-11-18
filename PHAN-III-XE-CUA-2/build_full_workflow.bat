@echo off
REM ============================================================
REM Build script cho XE-CUA-2 FilmAI Tool - Full Workflow v2.0
REM ============================================================
REM Tạo file EXE từ gui_app_full_workflow.py
REM Yêu cầu: Python 3.8+, PyInstaller
REM ============================================================

echo.
echo ========================================
echo  XE-CUA-2 FilmAI Tool - Full Workflow
echo  Build Script v2.0
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python chua duoc cai dat hoac chua them vao PATH!
    echo.
    echo Vui long:
    echo 1. Cai dat Python 3.8+ tu https://www.python.org/
    echo 2. Chon "Add Python to PATH" trong qua trinh cai dat
    echo.
    pause
    exit /b 1
)

echo [1/5] Checking Python... OK
echo.

REM Kiểm tra PyInstaller
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo [2/5] PyInstaller chua duoc cai dat. Dang cai dat...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo [ERROR] Khong the cai dat PyInstaller!
        pause
        exit /b 1
    )
) else (
    echo [2/5] Checking PyInstaller... OK
)
echo.

REM Kiểm tra dependencies
echo [3/5] Checking dependencies...
pip install -q google-generativeai
if %errorlevel% neq 0 (
    echo [WARNING] Khong the cai dat google-generativeai
)
echo.

REM Xóa build cũ
echo [4/5] Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "XE-CUA-2-FilmAI-FullWorkflow.spec" del "XE-CUA-2-FilmAI-FullWorkflow.spec"
echo.

REM Build EXE
echo [5/5] Building EXE with PyInstaller...
echo.
echo ----------------------------------------
echo  Building... Please wait...
echo ----------------------------------------
echo.

pyinstaller build_full_workflow.spec

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo  [ERROR] Build FAILED!
    echo ========================================
    echo.
    echo Loi thuong gap:
    echo - Thieu dependencies: chay "pip install -r requirements.txt"
    echo - Thieu file: kiem tra lai cac file .py va .json
    echo - Loi PyInstaller: thu update "pip install --upgrade pyinstaller"
    echo.
    pause
    exit /b 1
)

REM Kiểm tra file EXE
if exist "dist\XE-CUA-2-FilmAI-FullWorkflow.exe" (
    echo.
    echo ========================================
    echo  BUILD THANH CONG!
    echo ========================================
    echo.
    echo File EXE: dist\XE-CUA-2-FilmAI-FullWorkflow.exe
    echo.
    echo HUONG DAN SU DUNG:
    echo ------------------
    echo 1. Copy file EXE tu folder "dist" ra Desktop hoac thu muc bat ky
    echo 2. Copy cac file sau cung folder voi EXE:
    echo    - character_dictionary.json
    echo    - api_keys.txt (neu co)
    echo 3. Chay file EXE
    echo.
    echo LUU Y:
    echo ------
    echo - Lan dau mo se yeu cau nhap License Key
    echo - Cau hinh API Keys trong Settings
    echo - Doc HUONG_DAN_TAI_VA_SU_DUNG.md de biet them chi tiet
    echo.

    REM Mở folder dist
    echo Mo folder "dist"...
    explorer dist
) else (
    echo.
    echo [ERROR] Khong tim thay file EXE sau khi build!
    echo Kiem tra lai log ben tren de xem loi.
    echo.
)

echo.
pause

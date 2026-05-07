@echo off
title Khaservice Automation FULL PACKER - ITKHA
cd /d "%~dp0"

:: 1. Làm sạch thư mục cũ
if exist dist rd /s /q dist
if exist build rd /s /q build

:: Đảm bảo môi trường ảo có đầy đủ công cụ build
echo [1/4] Chuan bi moi truong build trong venv...
call .venv\Scripts\activate
python -m pip install --upgrade pip --quiet
python -m pip install pyinstaller playwright greenlet pandas openpyxl Pillow --quiet

echo [2/4] Dang chuan be trinh duyet Chromium...
set PLAYWRIGHT_BROWSERS_PATH=%~dp0pw-browser
python -m playwright install chromium

echo [3/4] Dang bat dau dong goi bang PyInstaller (VENV Mode)...
:: Build ở chế độ onedir để copy thư viện vào dễ dàng
python -m PyInstaller --noconfirm --onedir --windowed ^
    --name "BPAutoGachNo" ^
    --icon "Logo512.ico" ^
    --add-data "index.html;." ^
    --collect-all playwright ^
    --collect-all greenlet ^
    --hidden-import "greenlet._greenlet" ^
    --paths ".venv\Lib\site-packages" ^
    main.py

echo [4/4] Dang sao chep "nguyen khoi" thu vien vao ban build (FIX TRIET DE)...
:: Copy trình duyệt
xcopy "pw-browser" "dist\BPAutoGachNo\pw-browser" /E /I /Y

:: CHÉP ĐÈ TOÀN BỘ SITE-PACKAGES VÀO _INTERNAL
:: Cách này đảm bảo không bao giờ thiếu bất kỳ file .pyd hay .dll nào trên máy khách
xcopy ".venv\Lib\site-packages\*" "dist\BPAutoGachNo\_internal\" /E /I /Y /Q

echo.
echo ===================================================
echo DONE! Ban build "Sieu Ben" da san sang tai: [dist\BPAutoGachNo]
echo Moi thu vien da duoc chép tay vao de dam bao 100%% khong loi.
echo Bay gio hay mo Inno Setup va Compile file [itkha_installer.iss].
echo ===================================================
pause

@echo off
cd /d "%~dp0"
title Khaservice Automation FULL PACKER - ITKHA

:: XÃ³a bá» cache cÅ© Ä‘á»ƒ Ä‘Ã³ng gÃ³i má»›i hoÃ n toÃ n
if exist dist del /q dist\*
if exist build rd /s /q build

echo [1/4] Dang cai dat thu vien Python...
pip install pyinstaller playwright pandas openpyxl --quiet

echo [2/4] Dang tai Chromium vao thu muc [pw-browser]...
set PLAYWRIGHT_BROWSERS_PATH=pw-browser
playwright install chromium

echo [3/4] Dang bat dau dong goi (EXE se nang tam 200MB)...
:: --onefile: 1 file duy nhat
:: --windowed: Khong hien cua so den
:: --add-data: ChÃ¨n giao diá»‡n vÃ  trÃ¬nh duyá»‡t
:: --name: Äá»•i tÃªn file thÃ nh ITKHA.exe
pyinstaller --noconfirm --onefile --windowed ^
    --name "ITKHA" ^
    --add-data "index.html;." ^
    --add-data "pw-browser;pw-browser" ^
    main.py

echo.
echo ===================================================
echo DONE! File EXE cua ban da san sang tai: [dist\ITKHA.exe]
echo Copy file nay sang may khac va mo len de dung 1-Click.
echo ===================================================
pause

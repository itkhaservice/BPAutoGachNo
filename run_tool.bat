@echo off
title Khaservice Automation Tool
echo Dang kiem tra moi truong...

:: Kiem tra neu chua co thu vien thi cai dat
if not exist .venv (
    echo Khoi tao moi truong ao...
    python -m venv .venv
)

call .venv\Scripts\activate
echo Dang cai dat thu vien (neu thieu)...
pip install streamlit pandas playwright openpyxl --quiet
playwright install chromium

echo Dang khoi dong giao dien (Tab 1)...
streamlit run app.py
pause

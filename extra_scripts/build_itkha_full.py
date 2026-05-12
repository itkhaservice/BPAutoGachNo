import os
import subprocess
import sys
import shutil

def build_itkha():
    # Tên ứng dụng
    app_name = "BPAutoGachNo"
    main_script = "main.py"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(base_dir)

    if not os.path.exists(main_script):
        print(f"[!] Lỗi: Không tìm thấy file {main_script}")
        return

    # 1. Cài đặt các thư viện cần thiết
    print("[*] Đang kiểm tra thư viện...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "playwright", "pandas", "openpyxl", "--quiet"], check=True)

    # 2. Cài đặt Chromium vào thư mục cục bộ [pw-browser]
    print("[*] Đang kiểm tra trình duyệt Chromium...")
    env = os.environ.copy()
    env["PLAYWRIGHT_BROWSERS_PATH"] = "pw-browser"
    subprocess.run(["playwright", "install", "chromium"], env=env, check=True)

    # Lệnh build - Chuyển sang --onedir
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",
        "--windowed",
        f"--name={app_name}",
        "--add-data=app_ui.html;.",
        "--add-data=pw-browser;pw-browser",
        "--clean",
        "--noconfirm",
        main_script
    ]

    print(f"[*] Đang đóng gói {app_name} (One-Dir)...")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n[+] Đóng gói hoàn tất!")
        print(f"[+] Thư mục ứng dụng: {os.path.abspath(os.path.join('dist', app_name))}")
        print(f"[+] File chạy chính: {os.path.abspath(os.path.join('dist', app_name, app_name + '.exe'))}")
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Lỗi trong quá trình build: {e}")

if __name__ == "__main__":
    build_itkha()

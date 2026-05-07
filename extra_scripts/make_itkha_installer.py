import os
import subprocess
import winreg

def find_inno_setup():
    paths = [
        r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1",
        r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1"
    ]
    for path in paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                install_location = winreg.QueryValueEx(key, "InstallLocation")[0]
                iscc = os.path.join(install_location, "ISCC.exe")
                if os.path.exists(iscc):
                    return iscc
        except:
            continue
    return None

def make_installer():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    iss_file = "itkha_installer.iss"
    if not os.path.exists(iss_file):
        print(f"[!] Không tìm thấy file {iss_file}")
        return

    iscc_path = find_inno_setup()
    if not iscc_path:
        default_paths = [
            r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
            r"C:\Program Files\Inno Setup 6\ISCC.exe"
        ]
        for p in default_paths:
            if os.path.exists(p):
                iscc_path = p
                break
    
    if not iscc_path:
        print("[!] Không tìm thấy Inno Setup (ISCC.exe).")
        return

    print(f"[*] Đang biên dịch bộ cài đặt ITKHA bằng: {iscc_path}")
    try:
        subprocess.run([iscc_path, iss_file], check=True)
        print("\n" + "="*50)
        print("[+] THÀNH CÔNG! Bản cài đặt BPAutoGachNo đã sẵn sàng.")
        print(f"[+] File Setup: {os.path.abspath(os.path.join('Output', 'BPAutoGachNo_Setup.exe'))}")
        print("="*50)
    except Exception as e:
        print(f"[!] Lỗi khi biên dịch: {e}")

if __name__ == "__main__":
    make_installer()

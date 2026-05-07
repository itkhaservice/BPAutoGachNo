import os
import sys
import time
import json
import queue
import subprocess
from playwright.sync_api import sync_playwright

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def create_desktop_shortcut():
    """Tự động tạo Shortcut ngoài Desktop nếu chưa có."""
    if not getattr(sys, 'frozen', False):
        return # Không chạy khi đang dev

    exe_path = sys.executable
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    shortcut_path = os.path.join(desktop, 'BPAutoGachNo.lnk')

    if not os.path.exists(shortcut_path):
        try:
            ps_script = f'$s=(New-Object -COM WScript.Shell).CreateShortcut("{shortcut_path}");$s.TargetPath="{exe_path}";$s.Save()'
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
            print(">>> Da tao Shortcut ngoai Desktop.")
        except:
            pass

def find_chrome_executable():
    # Thá»© tá»± Æ°u tiÃªn: 
    # 1. ThÆ° má»¥c chá»©a file EXE (nhiá»u khi pw-browser náº±m ngoÃ i)
    # 2. ThÆ° má»¥c resource_path (khi dev hoáº·c náº¿u add-data)
    
    app_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(".")
    
    search_roots = [
        os.path.join(app_dir, "pw-browser"),
        resource_path("pw-browser"),
        app_dir,
        resource_path(".")
    ]
    
    for root_dir in search_roots:
        if not os.path.exists(root_dir): continue
        for root, dirs, files in os.walk(root_dir):
            if "chrome.exe" in files:
                exe_path = os.path.join(root, "chrome.exe")
                if "headless_shell" in exe_path: continue
                return exe_path
    return None

def start_gui():
    # Tao Shortcut ngay khi mo
    create_desktop_shortcut()

    task_queue = queue.Queue()
    chrome_exe = find_chrome_executable()

    # Tháº¿t láº­p biáº¿n mÃ´i trÆ°á»ng cho Playwright tÃ¬m trÃ¬nh duyá»‡t
    app_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(".")
    if os.path.exists(os.path.join(app_dir, "pw-browser")):
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(app_dir, "pw-browser")

    with sync_playwright() as p:
        print(f">>> [1] Khoi dong Playwright (Chrome: {chrome_exe})...")
        try:
            if chrome_exe:
                browser = p.chromium.launch(headless=False, executable_path=chrome_exe, args=["--start-maximized"])
            else:
                browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        except Exception as e:
            print(f">>> [!] Loi launch: {e}")
            # Fallback cuá»‘i cÃ¹ng
            try:
                browser = p.chromium.launch(headless=False, args=["--start-maximized"])
            except:
                # Náº¿u váº«n lá»—i thÃ¬ chá»‹u
                raise e

        # Context riêng cho GUI
        gui_context = browser.new_context(no_viewport=True)
        tab1 = gui_context.new_page()

        def ui_log(msg, color='#555'):
            try:
                tab1.evaluate("(args) => updateStatus(args.m, args.c)", {"m": msg, "c": color})
            except: pass

        def handle_start_click(email, password, data_list):
            task_queue.put({"email": email, "password": password, "data_list": data_list})
            return True

        tab1.expose_function("py_start_automation", handle_start_click)
        html_url = "file://" + resource_path("index.html").replace("\\", "/")
        tab1.goto(html_url)

        is_running = True
        browser.on("disconnected", lambda: globals().update(is_running=False))

        while is_running:
            try:
                task = task_queue.get_nowait()
                email, password, data_list = task["email"], task["password"], task["data_list"]

                ui_log(f"Dang khoi dong phien lam viec moi...")
                
                # Tạo Context MỚI hoàn toàn cho mỗi lần chạy (Incognito)
                auto_context = browser.new_context(no_viewport=True)
                tab2 = auto_context.new_page()
                
                try:
                    tab2.goto("https://qlvh.khaservice.com.vn/login", timeout=60000)
                    tab2.locator("//input[@name='email']").fill(str(email))
                    tab2.locator("//input[@name='password']").fill(str(password))
                    tab2.locator("//button[@type='submit']").click()

                    tab2.wait_for_selector("//a[@href='/fee-reports']", timeout=30000)
                    tab2.wait_for_timeout(2000)
                    tab2.locator("//a[@href='/fee-reports']").click()
                    tab2.wait_for_timeout(2000)
                    tab2.wait_for_load_state("networkidle")

                    for idx, row in enumerate(data_list):
                        canho, thang = str(row[0]), str(row[1])
                        ui_log(f"Dang xu ly {idx+1}/{len(data_list)}: {canho}")

                        try:
                            # 1. Chọn kỳ báo phí
                            tab2.locator("//*[@id='root']/div[2]/main/div/div/div[1]/div/span/div/div[2]/div/button[2]").click()
                            tab2.wait_for_selector("//*[@placeholder='MM/YYYY']", timeout=5000)
                            tab2.locator("//*[@placeholder='MM/YYYY']").fill(thang)
                            tab2.keyboard.press("Escape")
                            tab2.wait_for_timeout(500)

                            # 2. Tìm kiếm căn hộ
                            tab2.locator("//*[@id='input-search-list-style1']").fill(canho)
                            tab2.wait_for_timeout(1500)

                            # 3. Mở chi tiết
                            icon_view = tab2.locator("//*[@data-testid='VisibilityOutlinedIcon']").nth(1)       
                            icon_view.wait_for(state="visible", timeout=5000)
                            icon_view.click()

                            # --- LOGIC KIá»‚M TRA TRáº NG THÃI SAU KHI VÃ€O CHI TIáº¾T ---
                            dropdown_xpath = "//*[@id='simple-tabpanel-0']/div/div/div/form/div[2]/div[3]/div[2]/div"
                            tab2.wait_for_selector(dropdown_xpath, timeout=10000)

                            # Äá»£i má»™t chÃºt Ä‘á»ƒ UI cáº­p nháº­t dÆ° liau (trÃ¡nh trá»‘ng chá»¯)
                            tab2.wait_for_timeout(1000)
                            dropdown = tab2.locator(dropdown_xpath)
                            current_status = dropdown.inner_text().strip()

                            # Náº¿u tráº¡ng thÃ¡i ÄÃƒ LÃ€ "ÄÃ£ thanh toÃ¡n", thoÃ¡t ra ngay Ä‘á»ƒ trÃ¡nh spam
                            if "ÄÃ£ thanh toÃ¡n" in current_status:
                                ui_log(f"   [~] {canho}: Da thanh toan tu truoc. Chuyen tiep.", "orange")
                                tab2.locator("//*[@data-testid='ArrowBackIosNewIcon']").click()
                                continue


                            option_da_thanh_toan_xpath = "//li[@data-value='1']"
                            
                            max_retries = 3
                            success = False
                            for i in range(max_retries):
                                dropdown.click()
                                option_target = tab2.locator(option_da_thanh_toan_xpath)
                                option_target.wait_for(state="visible", timeout=3000)
                                option_target.click(force=True)

                                tab2.wait_for_timeout(1000)
                                if "Đã thanh toán" in dropdown.inner_text():
                                    success = True
                                    break
                                else:
                                    ui_log(f"   -> Thu lai lan {i+2} cho {canho}...", "orange")

                            if success:
                                tab2.locator("//*[@data-testid='SaveOutlinedIcon']").click()
                                tab2.wait_for_timeout(2000)
                                ui_log(f"   [+] {canho}: Thanh cong", "#108042")
                            else:
                                ui_log(f"   [!] {canho}: Khong the chon trang thái", "red")

                            tab2.locator("//*[@data-testid='ArrowBackIosNewIcon']").click()

                        except Exception as e:
                            print(f"Loi tai {canho}: {e}")
                            ui_log(f"   [!] Loi tai {canho}", "red")
                            try: tab2.locator("//*[@data-testid='ArrowBackIosNewIcon']").click()
                            except: pass

                        tab2.locator("//*[@id='input-search-list-style1']").fill("")
                        tab2.wait_for_timeout(500)

                    ui_log("✅ DA HOAN TAT!", "#108042")
                except Exception as e:
                    ui_log(f"Loi: {str(e)}", "red")
                finally:
                    # Tắt toàn bộ phiên làm việc automation ngay sau khi xong
                    try: tab2.close()
                    except: pass
                    try: auto_context.close()
                    except: pass
            except queue.Empty: pass

            try: tab1.wait_for_timeout(100)
            except: break

if __name__ == "__main__":
    start_gui()

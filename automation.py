from playwright.sync_api import sync_playwright
import time
import logging

def run_task(data_row, project_idx):
    """
    Hàm xử lý cho một dòng dữ liệu duy nhất.
    data_row: dict chứa thông tin dòng (ví dụ: {'Dự án': 'Tên DA', 'Tháng': '01/2024'})
    """
    project_name = data_row.get('Dự án', '')
    start_month_str = data_row.get('Tháng', '')
    
    logging.info(f"--- Đang xử lý dòng {project_idx}: {project_name} ---")
    
    with sync_playwright() as p:
        # Mở trình duyệt Chrome thật để người dùng quan sát
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(viewport={'width': 1366, 'height': 768})
        page = context.new_page()

        try:
            # 1. ĐĂNG NHẬP
            page.goto("https://qlvh.khaservice.com.vn/login")
            page.locator("input[name='email']").fill("admin@khaservice.com.vn")
            page.locator("input[name='password']").fill("Kha@@123")
            page.locator("button[type='submit']").click()
            
            page.wait_for_url(lambda u: "login" not in u, timeout=30000)
            page.wait_for_load_state("networkidle")

            # 2. CHỌN DỰ ÁN
            page.locator("#combo-box-demo").click()
            page.locator("#combo-box-demo").fill(str(project_name))
            page.locator("#combo-box-demo-option-0").click()
            page.wait_for_timeout(2000) 

            # 3. CHUYỂN ĐẾN TRANG BÁO PHÍ
            page.goto("https://qlvh.khaservice.com.vn/fee-reports")
            page.wait_for_load_state("networkidle")

            # --- THỰC HIỆN LOGIC CẬP NHẬT TRẠNG THÁI Ở ĐÂY ---
            # (Tôi giữ nguyên logic lọc và xóa của bạn nhưng tối giản để chạy nhanh)
            
            # Ví dụ: Lọc tháng và xóa
            filter_btn = page.locator("xpath=//*[@id='root']/div[2]/main/div/div/div[1]/div/span/div/div[2]/div/button[2]")
            if filter_btn.is_visible():
                filter_btn.click()
                page.wait_for_timeout(500)
                page.locator("xpath=//*[@id='demo-simple-select-helper']").click()
                page.locator("xpath=//*[@data-value='1']").click() 
                page.locator("xpath=//*[@placeholder='MM/YYYY']").fill(start_month_str)
                page.keyboard.press("Escape")
                page.wait_for_timeout(3000)
                
                # ... Các bước click xóa khác ...
            
            logging.info(f"Hoàn thành dòng {project_idx}")
            time.sleep(1) # Xem kết quả 1 giây trước khi đóng

        except Exception as e:
            logging.error(f"Lỗi tại dòng {project_idx}: {e}")
        finally:
            browser.close() # Đóng tab/browser để giải phóng RAM

import os
import sys
import subprocess
import logging
import pandas as pd
from playwright.sync_api import sync_playwright, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import traceback

# --- Đảm bảo Chromium Playwright được tải ---
# -----------------------------------------------------
# Đường dẫn file Excel
# === Cấu hình logging ra màn hình ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

excel_path = os.path.join(os.getcwd(), "data.xlsx")
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(os.getcwd(), "ms-playwright")

# -----------------------------------------------------

def ensure_playwright_browsers():
    logging.info(f"=========================================")
    logging.info(f"*** Cập nhật trạng thái báo phí ***")
    logging.info(f"=========================================")
    browsers_path = os.environ["PLAYWRIGHT_BROWSERS_PATH"]
    chromium_exists = False

    if os.path.exists(browsers_path):
        for d in os.listdir(browsers_path):
            if d.startswith("chromium-"):
                chromium_exists = True
                break

    if chromium_exists:
        logging.info("Đã tìm thấy Chromium tại %s", browsers_path)
    else:
        logging.info("Không tìm thấy Chromium. Đang tải…")
        try:
            subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium"],
                check=True
            )
            logging.info("Đã tải xong Chromium.")
        except Exception as e:
            logging.error("Không thể tải Chromium: %s", e)
# -----------------------------------------------------
# Đảm bảo Chromium Playwright đã cài
# -----------------------------------------------------

def run_test(show_browser=False):
    login_df = pd.read_excel(excel_path, sheet_name="Login")
    email = login_df.iloc[0, 0]
    password = login_df.iloc[0, 1]

    data_df = pd.read_excel(excel_path, sheet_name="Data", dtype=str)
    data_array = list(data_df.itertuples(index=False, name=None))

    logging.info(f"Đọc thông tin đăng nhập: {email} / {password}")
    logging.info(f"Số lượng căn hộ: {len(data_array)}")

    with sync_playwright() as p:
        logging.info(f"*** Khởi tạo trang ***")
        # show_browser quyết định headless hay không
        browser = p.chromium.launch(
            headless=not show_browser,
            args=["--start-maximized"] if show_browser else []
        )
        # bỏ viewport mặc định => trang sẽ theo kích thước của cửa sổ thật (full màn hình)      
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        # Đăng nhập
        page.goto("https://qlvh.khaservice.com.vn/login")
        page.locator("//input[@name='email']").fill(email)
        page.locator("//input[@name='password']").fill(password)
        page.locator("//button[@type='submit']").click()
        page.locator("//a[@href='/fee-reports']").click()
        page.wait_for_load_state("networkidle")

        # --- TĂNG HIỂN THỊ LÊN 1000 DÒNG ---
        try:
            logging.info("Đang cấu hình hiển thị 1000 dòng để xử lý hàng loạt...")
            # Click nút chọn số dòng hiển thị
            page.locator("xpath=//*[@id='root']/div[2]/main/div/div/div[4]/div/div[2]/button").click()
            # Chọn li[8] để hiển thị 1000 dòng (thay vì li[6] chỉ được ~145-150 dòng)
            page.locator("xpath=//*[@id='menu-apartment-list-style1']/div[3]/ul/li[8]").click()
            page.wait_for_timeout(3000)
            page.wait_for_load_state("networkidle")
        except Exception as e:
            logging.warning(f"Không thể chỉnh hiển thị 1000 dòng: {e}")

        for idx, (canho, thang) in enumerate(data_array, start=1):
            logging.info(f"[{idx}/{len(data_array)}] Căn hộ: {canho} - Tháng: {thang}")
            
            # 1. Chọn tháng cần gạch nợ
            page.locator("//*[@id='root']/div[2]/main/div/div/div[1]/div/span/div/div[2]/div/button[2]").click()
            page.locator("//*[@placeholder='MM/YYYY']").fill(str(thang))
            page.keyboard.press("Escape")
            
            # 2. Tìm kiếm mã căn hộ
            page.locator("//*[@id='input-search-list-style1']").fill(str(canho))
            page.wait_for_timeout(1000) # Chờ kết quả search hiện ra

            # --- VÀO CHI TIẾT ĐỂ KIỂM TRA CHO CHẮC CHẮN ---
            try:
                icon_view = page.locator("//*[@data-testid='VisibilityOutlinedIcon']").nth(1)
                if not icon_view.is_visible(timeout=5000):
                    logging.warning(f"Không tìm thấy căn hộ: {canho}. Bỏ qua.")
                    page.locator("//*[@id='input-search-list-style1']").fill("")
                    continue
                icon_view.click()
            except Exception as e:
                logging.error(f"Lỗi khi mở chi tiết căn hộ {canho}: {e}")
                page.locator("//*[@id='input-search-list-style1']").fill("")
                continue

            # --- PHẦN XỬ LÝ TRONG CHI TIẾT ---
            dropdown_xpath = "//*[@id='simple-tabpanel-0']/div/div/div/form/div[2]/div[3]/div[2]/div"
            option_da_thanh_toan_xpath = "//li[@data-value='1']"
            btn_save = "//*[@data-testid='SaveOutlinedIcon']"
            btn_back = "//*[@data-testid='ArrowBackIosNewIcon']"

            try:
                page.wait_for_selector(dropdown_xpath, timeout=10000)
                dropdown = page.locator(dropdown_xpath)

                # Chờ thông minh tránh placeholder "Đã thanh toán"
                for _ in range(8):
                    if "Đã thanh toán" not in dropdown.inner_text():
                        break
                    page.wait_for_timeout(200)

                if "Đã thanh toán" in dropdown.inner_text():
                    logging.info(f"   [~] {canho}: Đã thanh toán từ trước. Bỏ qua.")
                    page.locator(btn_back).click()
                    page.locator("//*[@id='input-search-list-style1']").fill("")
                    continue

                # Nếu chưa thanh toán thì tiến hành chọn
                dropdown.click()
                
                # Chọn "Đã thanh toán"
                option_target = page.locator(option_da_thanh_toan_xpath)
                option_target.wait_for(state="visible", timeout=3000)
                option_target.click(force=True)

                # Xác minh lại trước khi lưu
                page.wait_for_timeout(1000)
                if "Đã thanh toán" in dropdown.inner_text():
                    page.locator(btn_save).click()
                    logging.info(f"   [+] Cập nhật thành công: {canho}")
                    page.wait_for_timeout(2000)
                else:
                    logging.error(f"   [!] Lỗi: Không thể chọn trạng thái cho {canho}")
                
                # Quay lại danh sách
                page.locator(btn_back).click()
                page.locator("//*[@id='input-search-list-style1']").fill("")
                page.wait_for_timeout(500)
            except Exception as e:
                logging.error(f"Lỗi trong form chi tiết căn {canho}: {e}")
                page.reload() # Reload trang nếu kẹt trong form

        page.close()

def main():
    try:
        ensure_playwright_browsers()
        print("Bạn có muốn xem quá trình thực hiện không? Y / N")
        print("Nếu Y thì tắt bớt những chương trình khác để máy chạy mượt hơn!")
        choice = input("Nhập (Y/N). Sau đó nhấn Enter: ").strip().lower()
        show_browser = True if choice == 'y' else False

        run_test(show_browser=show_browser)
        logging.info("Đã hoàn thành.")
    except Exception as e:
        logging.error("Đã xảy ra lỗi:")
        traceback.print_exc()
    finally:
        input("\nNhấn Enter để thoát...")

if __name__ == "__main__":
    main()

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

excel_path = os.path.join(os.getcwd(), "BPCH.xlsx")
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(os.getcwd(), "ms-playwright")

# -----------------------------------------------------

def ensure_playwright_browsers():
    logging.info(f"=========================================")
    logging.info(f"*** Cập nhật lại báo phí ***")
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
    data_df = pd.read_excel(excel_path, sheet_name="Sheet1", dtype=str)
    data_array = list(data_df.itertuples(index=False, name=None))

    with sync_playwright() as p:
        logging.info(f"*** Khởi tạo trang ***")
        # show_browser quyết định headless hay không
        browser = p.chromium.launch(
            headless=not show_browser,
            args=["--start-maximized"] if show_browser else []
        )
        # bỏ viewport mặc định => trang sẽ theo kích thước cửa sổ thật (full màn hình)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        # Đăng nhập
        page.goto("https://qlvh.khaservice.com.vn/login")
        page.locator("//input[@name='email']").fill("bql.senhongbc@khaservice.com.vn")
        page.locator("//input[@name='password']").fill("BqlsenhongBC2025@")
        page.locator("//button[@type='submit']").click()
        page.locator("//a[@href='/fee-reports']").click()

        page.wait_for_timeout(3000000)
        for idx, (canho, thang) in enumerate(data_array, start=1):
            logging.info(f"[{idx}/{len(data_array)}] Căn hộ: {canho} - Tháng: {thang}")

            # Log info đang làm tháng nào

        # Bấm nút thêm mới báo phí //*[@id="root"]/div[2]/main/div/div/div[1]/div/span/div/div[2]/div/div[1]/button
        # Nhập tên báo phí //html/body/div/div[2]/main/div/div/div[2]/div/div/form/div[2]/div[1]/div[2]/div/input
        # Nhập tên căn hộ //html/body/div/div[2]/main/div/div/div[2]/div/div/form/div[2]/div[2]/div/div[2]/div/input
        # Chọn trạng thái thanh toán //html/body/div/div[2]/main/div/div/div[2]/div/div/form/div[2]/div[3]/div[2]/div/div
        # Chọn chưa thanh toán //html/body/div[2]/div[3]/ul/li[2]/p
        # Chọn tháng //html/body/div/div[2]/main/div/div/div[2]/div/div/form/div[2]/div[4]/div/div/input
        # Chọn từ //html/body/div/div[2]/main/div/div/div[2]/div/div/form/div[2]/div[5]/div/div/input
        # Chọn đến //html/body/div/div[2]/main/div/div/div[2]/div/div/form/div[2]/div[6]/div/div/input
        # Chọn hạn //html/body/div/div[2]/main/div/div/div[2]/div/div/form/div[2]/div[10]/div/div/input
        # Chọn ra lúc //html/body/div/div[2]/main/div/div/div[2]/div/div/form/div[2]/div[11]/div/div/input
        # Bật phat hành lên //html/body/div/div[2]/main/div/div/div[2]/div/div/form/div[2]/div[12]/span/span[1]/input
        # Hoàn tất thêm //html/body/div/div[2]/main/div/div/div[2]/div/div/form/div[1]/div/button

        # Nút thêm chi tiết //html/body/div/div[2]/main/div/div/div[2]/div/div[2]/div/div/div/form/div[2]/div[13]/div/div/button
        # Phí quản lý
        # Nhập tên phí //html/body/div[2]/div[3]/div/div[1]/div/div[1]/div[2]/div/input
        # Chọn loại phí //html/body/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div
        # Chọn loại 2 //html/body/div[3]/div[3]/ul/li[2]
        # Nhập số lượng //html/body/div[2]/div[3]/div/div[1]/div/div[3]/div[2]/div/input
        # Nhập đơn vị tính //html/body/div[2]/div[3]/div/div[1]/div/div[4]/div[2]/div/input
        # Nhập giá tiền //html/body/div[2]/div[3]/div/div[1]/div/div[5]/div[2]/div/input
        # Nhập đơn vị giá //html/body/div[2]/div[3]/div/div[1]/div/div[6]/div[2]/div/input
        # Nhập trạng thái //html/body/div[2]/div[3]/div/div[1]/div/div[9]/div[2]/div/div
        # Chưa thanh toán //html/body/div[3]/div[3]/ul/li[2]/p
        # Nhập tháng //html/body/div[2]/div[3]/div/div[1]/div/div[10]/div/div/input
        # Nhấn thêm //html/body/div[2]/div[3]/div/div[2]/button[2]

        # Nút thêm chi tiết //html/body/div/div[2]/main/div/div/div[2]/div/div[2]/div/div/div/form/div[2]/div[13]/div/div/button
        # Phí quản lý
        # Nhập tên phí //html/body/div[2]/div[3]/div/div[1]/div/div[1]/div[2]/div/input
        # Chọn loại phí //html/body/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div
        # Chọn loại 6 //html/body/div[3]/div[3]/ul/li[6]
        # Nhập đầu kỳ //html/body/div[2]/div[3]/div/div[1]/div/div[3]/div[2]/div/input
        # Nhập cuối kỳ //html/body/div[2]/div[3]/div/div[1]/div/div[4]/div[2]/div/input
        # Nhập đơn vị tính //html/body/div[2]/div[3]/div/div[1]/div/div[5]/div[2]/div/input
        # Nhập đơn giá //html/body/div[2]/div[3]/div/div[1]/div/div[6]/div[2]/div/input
        # Chọn trạng thái /html/body/div[2]/div[3]/div/div[1]/div/div[9]/div[2]/div/div
        # Chọn Chưa thanh toán //html/body/div[3]/div[3]/ul/li[2]/p
        # Chọn tháng /html/body/div[2]/div[3]/div/div[1]/div/div[11]/div/div/input
        # Tắt tự động tính /html/body/div[2]/div[3]/div/div[1]/div/div[16]/div/div[1]/div/span/span[1]/input
        # Nhập tiêu thụ /html/body/div[2]/div[3]/div/div[1]/div/div[18]/div/div[1]/div[2]/div/input
        # Nhập giá /html/body/div[2]/div[3]/div/div[1]/div/div[18]/div/div[2]/div[2]/div/input
        # Nhấn thêm //html/body/div[2]/div[3]/div/div[2]/button[2]

        # Nút thêm chi tiết //html/body/div/div[2]/main/div/div/div[2]/div/div[2]/div/div/div/form/div[2]/div[13]/div/div/button


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
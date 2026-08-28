import pytest
import shutil
import datetime
from playwright.sync_api import sync_playwright
from pages.user_page import UserPage
from config import PLATFORMS, global_data


class TestUser:
    @pytest.mark.order(3)
    def test_user_flow(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                record_video_dir="videos/",
                record_video_size={"width": 1920, "height": 1080}
            )
            page = context.new_page()

            user = UserPage(page)
            user.login(
                PLATFORMS["user"]["username"],
                PLATFORMS["user"]["password"]
            )
            order_number = user.buy_resource()

            global_data["order_number"] = order_number
            with open("latest_order.txt", "w", encoding="utf-8") as f:
                f.write(order_number)

            video = context.pages[0].video
            context.close()
            browser.close()

            today = datetime.datetime.now().strftime("%Y%m%d")
            video_name = f"test_03_user_{today}.webm"
            shutil.move(video.path(), f"videos/{video_name}")
            print(f"📹 视频已保存: videos/{video_name}")

            assert True

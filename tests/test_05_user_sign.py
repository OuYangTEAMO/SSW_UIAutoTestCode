import pytest
import shutil
import datetime
from playwright.sync_api import sync_playwright
from pages.user_page import UserPage
from config import PLATFORMS, global_data


class TestUserSign:
    @pytest.mark.order(5)
    def test_user_sign_flow(self):
        order_no = global_data.get("order_number")
        assert order_no is not None, "未获取到订单编号"

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
            user.sign_order(order_no)

            video = context.pages[0].video
            context.close()
            browser.close()

            today = datetime.datetime.now().strftime("%Y%m%d")
            video_name = f"test_05_user_sign_{today}.webm"
            shutil.move(video.path(), f"videos/{video_name}")
            print(f"📹 视频已保存: videos/{video_name}")

            assert True

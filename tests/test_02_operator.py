import pytest
import shutil
import datetime
from playwright.sync_api import sync_playwright
from pages.operator_page import OperatorPage
from config import PLATFORMS


class TestOperator:
    @pytest.mark.order(2)
    def test_operator_flow(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                record_video_dir="videos/",
                record_video_size={"width": 1920, "height": 1080}
            )
            page = context.new_page()

            operator = OperatorPage(page)
            operator.login(
                PLATFORMS["operator"]["username"],
                PLATFORMS["operator"]["password"]
            )
            operator.approve_resource_publish()

            video = context.pages[0].video
            context.close()
            browser.close()

            today = datetime.datetime.now().strftime("%Y%m%d")
            video_name = f"test_02_operator_{today}.webm"
            shutil.move(video.path(), f"videos/{video_name}")
            print(f"📹 视频已保存: videos/{video_name}")

            assert True

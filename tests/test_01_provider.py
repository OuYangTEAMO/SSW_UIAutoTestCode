import pytest
import shutil
import datetime
from playwright.sync_api import sync_playwright
from pages.provider_page import ProviderPage
from config import PLATFORMS


class TestProvider:
    @pytest.mark.order(1)
    def test_provider_flow(self):
        video_name = None
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                record_video_dir="videos/",
                record_video_size={"width": 1920, "height": 1080}
            )
            page = context.new_page()

            provider = ProviderPage(page)
            provider.login(
                PLATFORMS["provider"]["username"],
                PLATFORMS["provider"]["password"]
            )
            provider.create_datasource()
            provider.create_resource()
            provider.mount_data()
            provider.publish_resource()

            # 保存视频路径用于重命名
            video = context.pages[0].video
            context.close()
            browser.close()

            # 重命名视频文件：test_01_provider_YYYYMMDD.mp4
            today = datetime.datetime.now().strftime("%Y%m%d")
            video_name = f"test_01_provider_{today}.webm"
            shutil.move(video.path(), f"videos/{video_name}")
            print(f"📹 视频已保存: videos/{video_name}")

            assert True

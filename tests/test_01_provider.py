import pytest
from playwright.sync_api import sync_playwright
from pages.provider_page import ProviderPage
from config import PLATFORMS


class TestProvider:
    @pytest.mark.order(1)
    def test_provider_flow(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(record_video_dir="videos/")
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

            context.close()
            browser.close()
            assert True

import pytest
from playwright.sync_api import sync_playwright
from pages.provider_page import ProviderPage
from config import PLATFORMS, global_data


class TestProviderSign:
    @pytest.mark.order(6)
    def test_provider_sign_flow(self):
        order_no = global_data.get("order_number")
        assert order_no is not None, "未获取到订单编号"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(record_video_dir="videos/")
            page = context.new_page()

            provider = ProviderPage(page)
            provider.login(
                PLATFORMS["provider"]["username"],
                PLATFORMS["provider"]["password"]
            )
            provider.sign_order(order_no)

            context.close()
            browser.close()
            assert True

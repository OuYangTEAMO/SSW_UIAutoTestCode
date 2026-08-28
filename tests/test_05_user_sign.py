import pytest
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
            context = browser.new_context(record_video_dir="videos/")
            page = context.new_page()

            user = UserPage(page)
            user.login(
                PLATFORMS["user"]["username"],
                PLATFORMS["user"]["password"]
            )
            user.sign_order(order_no)

            context.close()
            browser.close()
            assert True

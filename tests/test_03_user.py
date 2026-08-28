import pytest
from playwright.sync_api import sync_playwright
from pages.user_page import UserPage
from config import PLATFORMS, global_data


class TestUser:
    @pytest.mark.order(3)
    def test_user_flow(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(record_video_dir="videos/")
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

            context.close()
            browser.close()
            assert True

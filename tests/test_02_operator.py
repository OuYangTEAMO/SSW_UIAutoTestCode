import pytest
from playwright.sync_api import sync_playwright
from pages.operator_page import OperatorPage
from config import PLATFORMS


class TestOperator:
    @pytest.mark.order(2)
    def test_operator_flow(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(record_video_dir="videos/")
            page = context.new_page()

            operator = OperatorPage(page)
            operator.login(
                PLATFORMS["operator"]["username"],
                PLATFORMS["operator"]["password"]
            )
            operator.approve_resource_publish()

            context.close()
            browser.close()
            assert True

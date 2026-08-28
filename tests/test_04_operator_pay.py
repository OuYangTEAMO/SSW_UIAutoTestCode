import pytest
from playwright.sync_api import sync_playwright
from pages.operator_page import OperatorPage
from config import PLATFORMS, global_data


class TestOperatorPay:
    @pytest.mark.order(4)
    def test_operator_pay_flow(self):
        order_no = global_data.get("order_number")
        assert order_no is not None, "未获取到订单编号"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(record_video_dir="videos/")
            page = context.new_page()

            operator = OperatorPage(page)
            operator.login(
                PLATFORMS["operator"]["username"],
                PLATFORMS["operator"]["password"]
            )
            operator.approve_order_payment(order_no)

            context.close()
            browser.close()
            assert True

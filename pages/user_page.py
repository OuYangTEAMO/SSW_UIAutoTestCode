import re
from playwright.sync_api import Page
from pages.base_page import BasePage
from config import TEST_DATA


class UserPage(BasePage):
    """使用方平台页面操作"""

    def login(self, username: str, password: str):
        """登录使用方平台"""
        self.goto("https://usernet.mayishangshu.cn:82/login?redirect=/home")
        self.get_by_role("textbox", name="请输入账号").click()
        self.get_by_role("textbox", name="请输入账号").fill(username)
        self.get_by_role("textbox", name="请输入密码").click()
        self.get_by_role("textbox", name="请输入密码").fill(password)
        self.get_by_role("button", name="登 录").click()

    def buy_resource(self) -> str:
        """购买数据资源，返回订单编号"""
        # 进入数据资源目录
        self.page.get_by_role("listitem", name="数据资源目录").click()
        self.page.get_by_role("row").filter(
            has_text=f"{TEST_DATA['resource_name']}"
        ).get_by_role("button", name="购买").first.click()
        self.page.get_by_role("button", name="确 定").click()

        # 获取订单编号
        self.page.get_by_role("listitem", name="采购订单").click()
        self.wait_for_timeout(2000)

        row = self.page.get_by_role("row").filter(has_text=TEST_DATA["resource_name"]).first
        headers = self.page.locator("table thead th").all_inner_texts()
        order_index = headers.index("订单编号")
        order_cell = row.locator(f"td:nth-child({order_index + 1})")
        order_number = order_cell.inner_text().strip()

        assert order_number != "", "订单编号为空！"
        assert order_number.startswith("cpdd"), f"订单编号格式不正确: {order_number}"

        print(f"📌 获取到订单编号: {order_number}")
        return order_number

    def sign_order(self, order_no: str):
        """使用方签约"""
        self.page.get_by_role("listitem", name="采购订单").click()
        self.wait_for_timeout(2000)
        self.page.get_by_role("row").filter(
            has_text=order_no
        ).first.get_by_role("button", name="签约").click()
        self.page.get_by_role("radio", name="签约").check()
        self.page.get_by_role("button", name="确 定").click()
        print(f"✅ 使用方签约完成！订单号: {order_no}")

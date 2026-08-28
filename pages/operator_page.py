import re
from playwright.sync_api import Page
from pages.base_page import BasePage
from config import TEST_DATA


class OperatorPage(BasePage):
    """运营方平台页面操作"""

    def login(self, username: str, password: str):
        """登录运营方平台"""
        self.goto("https://tds.mayishangshu.cn:82/login?redirect=/home")
        self.get_by_role("textbox", name="请输入账号").click()
        self.get_by_role("textbox", name="请输入账号").fill(username)
        self.get_by_role("textbox", name="请输入密码").click()
        self.get_by_role("textbox", name="请输入密码").fill(password)
        self.get_by_role("button", name="登 录").click()
        print("✅ operator 登录成功！")

    def approve_resource_publish(self):
        """审批数据资源上架"""
        self._enter_todo()

        # 审批资源上架
        self.page.get_by_role("row").filter(
            has_text=f"{TEST_DATA['resource_name']} 上架"
        ).first.get_by_role("button", name="办理").click()
        self.page.get_by_role("button", name="开始办理").click()
        self.wait_for_timeout(3000)
        self.page.locator(".cover-btn").click()
        self.wait_for_timeout(1000)
        self.page.get_by_role("textbox", name="请输入").fill("没意见")
        self.page.get_by_role("button", name="同 意").click()
        self.page.get_by_role("button", name="确 定").click()
        self.wait_for_timeout(3000)
        print(f"✅ 数据资源 {TEST_DATA['resource_name']} 审批上架完成！")

    def approve_order_payment(self, order_no: str):
        """审批交易订单支付"""
        self._enter_todo()

        # 审批交易订单
        self.page.get_by_role("row").filter(
            has_text=order_no
        ).first.get_by_role("button", name="办理").click()
        self.page.get_by_role("button", name="开始办理").click()
        self.wait_for_timeout(3000)
        self.page.locator(".cover-btn").click()
        self.wait_for_timeout(1000)
        self.page.get_by_role("textbox", name="请输入").fill("没意见")
        self.page.get_by_role("button", name="同 意").click()
        self.page.get_by_role("button", name="确 定").click()
        print(f"✅ 交易订单 {order_no} 审批支付完成！")

    def _enter_todo(self):
        """进入待办事项"""
        self.page.locator("div").filter(has_text=re.compile(r"^待办已办$")).click()
        self.page.get_by_role("listitem", name="待办事项").click()

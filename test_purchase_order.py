import re
import pytest
from playwright.sync_api import sync_playwright

from config import global_data


class TestPurchaseOrder:
    """
    独立订单购买+审批+签约全流程测试
    不依赖提供方/运营方前置流程，直接购买固定资源并完成全流程
    """

    # ==================== 固定资源名称（可修改） ====================
    FIXED_RESOURCE_NAME = "Auto_数据服务_Resource_MySQL_0901_4103"
    # FIXED_RESOURCE_NAME = "Auto_安全沙盒_Resource_MySQL_0901_5654"
    # FIXED_RESOURCE_NAME = "Auto_隐私计算_Resource_MySQL_0901_4907"

    @pytest.mark.order(1)
    def test_purchase_full_flow(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(record_video_dir="videos/")
            page = context.new_page()

            # =========================================================
            # 第1步：使用方登录 → 购买资源 → 获取订单号
            # =========================================================
            self._step_purchase_order(page)

            # =========================================================
            # 第2步：运营方登录 → 审批订单 → 确认支付
            # =========================================================
            # 清除登录态，切换到运营方
            context.clear_cookies()
            self._step_operator_approve(page)

            # =========================================================
            # 第3步：使用方登录 → 签约
            # =========================================================
            context.clear_cookies()
            self._step_user_sign(page)

            # =========================================================
            # 第4步：提供方登录 → 签约
            # =========================================================
            context.clear_cookies()
            self._step_provider_sign(page)

            # =========================================================
            # 完成
            # =========================================================
            print("\n🎉 订单购买+审批+签约全流程执行完毕！")
            context.close()
            browser.close()
            assert True

    # ==================== 各步骤方法 ====================

    def _step_purchase_order(self, page):
        """第1步：使用方购买资源，获取订单号"""
        print("\n" + "=" * 50)
        print("【第1步】使用方购买资源")
        print("=" * 50)

        # 登录使用方平台
        page.goto("https://usernet.mayishangshu.cn:82/login?redirect=/home")
        page.get_by_role("textbox", name="请输入账号").fill("18277778811")
        page.get_by_role("textbox", name="请输入密码").fill("654321")
        page.get_by_role("button", name="登 录").click()
        print("✅ 使用方登录成功！")

        # 进入数据资源目录，购买固定资源
        page.get_by_role("listitem", name="数据资源目录").click()
        page.get_by_role("row").filter(
            has_text=self.FIXED_RESOURCE_NAME
        ).get_by_role("button", name="购买").first.click()
        page.get_by_role("button", name="确 定").click()
        print(f"✅ 已购买资源: {self.FIXED_RESOURCE_NAME}")

        # 进入采购订单，获取订单编号
        page.get_by_role("listitem", name="采购订单").click()
        page.wait_for_timeout(2000)

        row = page.get_by_role("row").filter(has_text=self.FIXED_RESOURCE_NAME).first
        headers = page.locator("table thead th").all_inner_texts()
        order_index = headers.index("订单编号")
        order_cell = row.locator(f"td:nth-child({order_index + 1})")
        order_number = order_cell.inner_text().strip()

        # 断言验证
        assert order_number != "", "订单编号为空！"
        assert order_number.startswith("cpdd"), f"订单编号格式不正确: {order_number}"

        # 存入 global_data
        global_data["order_number"] = order_number
        print(f"📌 获取到订单编号: {order_number}")
        print(f"✅ 订单编号 {order_number} 已保存")

    def _step_operator_approve(self, page):
        """第2步：运营方审批订单 + 确认支付"""
        print("\n" + "=" * 50)
        print("【第2步】运营方审批订单")
        print("=" * 50)

        # 登录运营方平台
        page.goto("https://tds.mayishangshu.cn:82/login?redirect=/home")
        page.get_by_role("textbox", name="请输入账号").fill("Presenter")
        page.get_by_role("textbox", name="请输入密码").fill("0000")
        page.get_by_role("button", name="登 录").click()
        print("✅ 运营方登录成功！")

        # 进入待办事项
        page.locator("div").filter(has_text=re.compile(r"^待办已办$")).click()
        page.get_by_role("listitem", name="待办事项").click()

        # 找到交易订单，点击办理
        order_no = global_data.get("order_number")
        page.get_by_role("row").filter(has_text=order_no).first.get_by_role("button", name="办理").click()
        print(f"🔍 已找到订单 {order_no}，点击办理")

        # 开始办理
        page.get_by_role("button", name="开始办理").click()
        page.wait_for_timeout(2000)

        # 填写审批意见
        page.locator(".cover-btn").click()
        page.wait_for_timeout(500)
        page.get_by_role("textbox", name="请输入").fill("审批通过")
        page.get_by_role("button", name="同 意").click()
        page.get_by_role("button", name="确 定").click()
        print(f"✅ 交易订单 {order_no} 审批完成！")

    def _step_user_sign(self, page):
        """第3步：使用方签约"""
        print("\n" + "=" * 50)
        print("【第3步】使用方签约")
        print("=" * 50)

        # 进入使用方平台
        page.goto("https://usernet.mayishangshu.cn:82/login?redirect=/home")
        # page.get_by_role("textbox", name="请输入账号").fill("18277778811")
        # page.get_by_role("textbox", name="请输入密码").fill("654321")
        # page.get_by_role("button", name="登 录").click()
        # print("✅ 使用方登录成功！")

        # 进入采购订单
        order_no = global_data.get("order_number")
        page.get_by_role("listitem", name="采购订单").click()
        page.wait_for_timeout(2000)

        # 找到订单，点击签约
        page.get_by_role("row").filter(has_text=order_no).first.get_by_role("button", name="签约").click()
        print(f"🔍 已找到订单 {order_no}，点击签约")

        # 确认签约
        page.get_by_role("radio", name="签约").check()
        page.get_by_role("button", name="确 定").click()
        print(f"✅ 使用方签约完成！订单号: {order_no}")

    def _step_provider_sign(self, page):
        """第4步：提供方签约"""
        print("\n" + "=" * 50)
        print("【第4步】提供方签约")
        print("=" * 50)

        # 登录提供方平台
        page.goto("https://providernet.mayishangshu.cn:82/login?redirect=/home")
        page.get_by_role("textbox", name="请输入账号").fill("18277778800")
        page.get_by_role("textbox", name="请输入密码").fill("654321")
        page.get_by_role("button", name="登 录").click()
        print("✅ 提供方登录成功！")

        # 进入数据资源订单
        order_no = global_data.get("order_number")
        page.locator("div").filter(has_text=re.compile(r"^数据提供$")).click()
        page.get_by_role("listitem", name="数据资源订单").click()
        page.wait_for_timeout(2000)

        # 找到订单，点击签约
        page.get_by_role("row").filter(has_text=order_no).first.get_by_role("button", name="签约").click()
        print(f"🔍 已找到订单 {order_no}，点击签约")

        # 确认签约
        page.get_by_role("radio", name="签约").check()
        page.get_by_role("button", name="确 定").click()
        print(f"✅ 提供方签约完成！订单号: {order_no}")


# ==================== 直接运行入口 ====================
if __name__ == "__main__":
    # 使用 pytest 运行当前文件
    import sys
    sys.exit(pytest.main([__file__, "-v", "-s"]))
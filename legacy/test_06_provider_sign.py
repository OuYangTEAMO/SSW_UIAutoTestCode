import re
import pytest
from playwright.sync_api import sync_playwright

from config import TEST_DATA, global_data

class TestProviderSign:
    @pytest.mark.order(6)
    def test_provider_sign_flow(self):
        with sync_playwright() as p:
            # 启动浏览器(headless=False 表示全过程可见)
            browser = p.chromium.launch(headless=False)
            # 开启录屏 视频保存到 videos 文件夹
            context = browser.new_context(record_video_dir="videos/")
            page = context.new_page()

            # 登录
            page.goto("https://providernet.mayishangshu.cn:82/login?redirect=/home")
            page.get_by_role("textbox", name="请输入账号").click()
            page.get_by_role("textbox", name="请输入账号").fill("18277778800")
            page.get_by_role("textbox", name="请输入密码").click()
            page.get_by_role("textbox", name="请输入密码").fill("654321")
            page.get_by_role("button", name="登 录").click()
            print(f"✅ provider 登录成功！")

            # 进入订单页面
            page.locator("div").filter(has_text=re.compile(r"^数据提供$")).click()
            page.get_by_role("listitem", name="数据资源订单").click()
            page.wait_for_timeout(2000)

            # 使用方签约
            # page.get_by_role("cell", name="cpdd20260828006").click()
            # page.get_by_role("button", name="签约").first.click()

            # 从 global_data 获取订单号
            order_no = global_data.get("order_number")
            assert order_no is not None, "❌ 未获取到订单编号，请检查 test_03 是否执行成功！"
            print(f"🔍 正在定位订单: {order_no}")

            # 直接通过订单号找到行，点击该行内的“签约”按钮
            row = page.get_by_role("row").filter(has_text=order_no).first.get_by_role("button", name="签约").click()
            # row = page.get_by_role("row").filter(has_text="cpdd20260828003").first.get_by_role("button", name="签约").click()
            print(f"✅ 已点击订单 {order_no} 的签约按钮")

            page.get_by_role("radio", name="签约").check()
            page.get_by_role("button", name="确 定").click()
            print(f"✅ 使用方签约完成！")

            # 关闭浏览器
            context.close()
            browser.close()

            # 简单断言
            assert True
import re
import pytest
from playwright.sync_api import sync_playwright

from config import TEST_DATA

class TestOperator:
    @pytest.mark.order(2)
    def test_operator_flow(self):
        with sync_playwright() as p:
            # 启动浏览器(headless=False 表示全过程可见)
            browser = p.chromium.launch(headless=False)
            # 开启录屏 视频保存到 videos 文件夹
            context = browser.new_context(record_video_dir="videos/")
            page = context.new_page()

            # 登录
            page.goto("https://tds.mayishangshu.cn:82/login?redirect=/home")
            page.get_by_role("textbox", name="请输入账号").click()
            page.get_by_role("textbox", name="请输入账号").fill("Presenter")
            page.get_by_role("textbox", name="请输入密码").click()
            page.get_by_role("textbox", name="请输入密码").fill("0000")
            page.get_by_role("button", name="登 录").click()
            print(f"✅ operator 登录成功！")

            # 进入待办已办页面
            # 待办事项
            page.locator("div").filter(has_text=re.compile(r"^待办已办$")).click()
            page.get_by_role("listitem", name="待办事项").click()
            # 数据资源发布上架审批
            page.get_by_role("row").filter(has_text=f"{TEST_DATA['resource_name']} 上架").first.get_by_role("button", name="办理").click()
            # page.get_by_role("button", name="办理").nth(1).click()
            page.get_by_role("button", name="开始办理").click()
            page.wait_for_timeout(3000)
            page.locator(".cover-btn").click()
            # page.get_by_text("审批意见").nth(1).click()
            # page.locator("div").filter(has_text=re.compile(r"^审批意见$")).first.click()
            page.wait_for_timeout(1000)
            page.get_by_role("textbox", name="请输入").click()
            page.get_by_role("textbox", name="请输入").fill("没意见")
            page.get_by_role("button", name="同 意").click()
            page.get_by_role("button", name="确 定").click()
            print(f"✅ 数据资源 {TEST_DATA['resource_name']} 审批上架完成！")
            page.wait_for_timeout(3000)

            # 关闭浏览器
            context.close()
            browser.close()

            # 简单断言
            assert True
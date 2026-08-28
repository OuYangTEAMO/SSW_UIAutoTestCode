import pytest
from playwright.sync_api import sync_playwright
from config import TEST_DATA, global_data

class TestUser:
    @pytest.mark.order(3)
    def test_user_flow(self):
        with sync_playwright() as p:
            # 启动浏览器(headless=False 表示全过程可见)
            browser = p.chromium.launch(headless=False)
            # 开启录屏 视频保存到 videos 文件夹
            context = browser.new_context(record_video_dir="videos/")
            page = context.new_page()

            # 登录
            page.goto("https://usernet.mayishangshu.cn:82/login?redirect=/home")
            page.get_by_role("textbox", name="请输入账号").click()
            page.get_by_role("textbox", name="请输入账号").fill("18277778811")
            page.get_by_role("textbox", name="请输入密码").click()
            page.get_by_role("textbox", name="请输入密码").fill("654321")
            page.get_by_role("button", name="登 录").click()

            # 进入数据使用页面
            # 购买数据资源
            page.get_by_role("listitem", name="数据资源目录").click()
            page.get_by_role("row").filter(has_text=f"{TEST_DATA['resource_name']}").get_by_role("button", name="购买").first.click()
            # page.get_by_role("row").filter(has_text="Auto_Resource_MySQL_0827_4821").get_by_role("button", name="购买").first.click()
            page.get_by_role("button", name="确 定").click()

            # 采购订单获取订单编号 → 传给 operator 进行该订单审批
            # 购买完成后，进入采购订单页面获取订单编号
            page.get_by_role("listitem", name="采购订单").click()
            page.wait_for_timeout(2000)
            # 根据数据资源名称获取最新订单编号
            resource_name = TEST_DATA["resource_name"]
            # 找到包含该资源名称的第一行（最新的一条）
            row = page.get_by_role("row").filter(has_text=resource_name).first
            # row = page.get_by_role("row").filter(has_text="Auto_Resource_MySQL_0827_4821").first
            # 获取订单编号（不在第一列）
            # 先获取表头，找到"订单编号"所在的列索引
            headers = page.locator("table thead th").all_inner_texts()
            order_index = headers.index("订单编号")  # 找到"订单编号"列的索引
            # 找到包含资源名称的行，取该行的订单编号列
            order_cell = row.locator(f"td:nth-child({order_index + 1})")  # 索引从1开始
            order_number = order_cell.inner_text().strip()
            print(f"📌 获取到订单编号: {order_number}")

            # 确保获取到了有效值
            assert order_number != "", "订单编号为空！"
            assert order_number.startswith("cpdd"), f"订单编号格式不正确: {order_number}"

            # 存入 global_data，供运营方审批使用
            global_data["order_number"] = order_number
            print(f"✅ 订单编号 {order_number} 已保存")

            # 保存到文本文件
            with open("latest_order.txt", "w", encoding="utf-8") as f:
                f.write(order_number)

            # 关闭浏览器
            context.close()
            browser.close()

            # 简单断言 证明跑完
            assert True
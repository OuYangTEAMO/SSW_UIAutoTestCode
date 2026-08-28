import re
import pytest 
from playwright.sync_api import sync_playwright

from config import TEST_DATA, SAMPLE_FILE, COVER_IMAGE


class TestProvider:
    @pytest.mark.order(1)
    def test_provider_flow(self):
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

            # 进入数据源管理页面
            page.get_by_role("listitem", name="数据源").click()
            page.locator(".icon-ym.icon-ym-nav-home-fill").click()
            page.locator("div").filter(has_text=re.compile(r"^数据资产管理$")).click()
            page.locator("div").filter(has_text=re.compile(r"^数据资产管理$")).click()
            page.get_by_role("listitem", name="数据源").click()

            # 新增数据源
            page.get_by_role("button", name=" 新增").click()
            page.get_by_role("textbox", name="* 数据源名称").click()
            page.get_by_role("textbox", name="* 数据源名称").fill(TEST_DATA["datasource_name"])
            page.get_by_role("combobox", name="* 数据源类型").click()
            page.locator("[id=\"711927340971634757\"]").get_by_text("MySQL", exact=True).click()
            page.get_by_role("textbox", name="* 地址 question-circle").click()
            page.get_by_role("textbox", name="* 地址 question-circle").fill("192.168.1.15")
            page.get_by_role("textbox", name="* 端口").click()
            page.get_by_role("textbox", name="* 端口").fill("1966")
            page.get_by_role("textbox", name="* 数据库").click()
            page.get_by_role("textbox", name="* 数据库").fill("test")
            page.get_by_role("textbox", name="* 用户名").click()
            page.get_by_role("textbox", name="* 用户名").fill("root")
            page.get_by_role("textbox", name="* 密码").click()
            page.get_by_role("textbox", name="* 密码").fill("2213")
            page.get_by_role("button", name="连接测试").click()
            page.wait_for_selector("text=数据库连接成功", timeout=10000) 
            page.get_by_role("button", name="确 定").click()
            page.wait_for_selector("text=新建成功", timeout=10000) 

            # 启用数据源
            page.locator(".table-settings > .anticon > svg").first.click()
            page.get_by_role("button", name="启用").first.click()

            # 强制等待1秒，确保启用操作完成
            page.wait_for_timeout(1000)
            print(f"✅ 数据源 {TEST_DATA['datasource_name']} 创建并启用成功！")

            # 进入数据源管理页面
            page.get_by_role("listitem", name="数据资源").click()

            # 新增数据资源
            page.get_by_role("button", name=" 新增").click()
            page.get_by_role("textbox", name="* 数据资源名称").click()
            page.get_by_role("textbox", name="* 数据资源名称").fill(TEST_DATA["resource_name"])
            page.get_by_role("combobox", name="* 来源类型").click()
            page.get_by_text("原始取得").click()
            page.get_by_role("combobox", name="* 安全等级").click()
            page.get_by_text("公开数据，无安全保护要求").click()
            page.get_by_role("textbox", name="资源简介").click()
            page.get_by_role("textbox", name="资源简介").fill("随便写的简介")
            page.locator("iframe[title=\"Rich Text Area\"]").content_frame.locator("html").click()
            page.locator("iframe[title=\"Rich Text Area\"]").content_frame.get_by_label("编辑区。按Alt+0键打开帮助。").fill("随便写的资源详情")
            page.get_by_role("button", name="确 定").click()
            page.locator(".table-settings > .anticon > svg").first.click()
            page.wait_for_timeout(3000)
            print(f"✅ 新增数据资源 {TEST_DATA['resource_name']} 完成！")

            # 挂载数据
            page.get_by_role("button", name="挂载数据").first.click()
            page.wait_for_timeout(2000)
            # 选择刚才创建的数据源
            page.locator("div").filter(has_text=re.compile(r"^请选择$")).nth(5).click()
            page.get_by_role("row", name=f"{TEST_DATA['datasource_name']} MySQL").get_by_label("", exact=True).check()
            page.get_by_label("选择数据").get_by_role("button", name="确 定").click()
            # 输入数据集名称和SQL语句
            page.get_by_role("textbox", name="数据集名称").click()
            page.get_by_role("textbox", name="数据集名称").fill(f"{TEST_DATA['resource_name']}_dataset")
            page.get_by_role("textbox", name="sql语句").click()
            page.get_by_role("textbox", name="sql语句").fill("select * from desensitization")
            page.wait_for_timeout(2000)
            # 添加脱敏规则  tel字段掩码脱敏
            page.get_by_title("添加").nth(1).click()
            page.get_by_role("textbox", name="请输入").nth(4).click()
            page.get_by_role("textbox", name="请输入").nth(4).fill("tel")
            page.locator("div").filter(has_text=re.compile(r"^请选择$")).nth(1).click()
            page.get_by_text("字符串").click()
            page.get_by_role("cell", name="请选择").click()
            page.get_by_text("掩码").click()
            page.get_by_role("textbox", name="请输入").nth(5).click()
            page.get_by_role("textbox", name="请输入").nth(5).fill("2-9")
            page.get_by_role("button", name="数据测试").click()
            page.wait_for_timeout(2000)
            # 上传样例文件
            if not SAMPLE_FILE.exists():
                print(f"样例文件不存在: {SAMPLE_FILE}")
            else:
                page.locator("input[type='file']").set_input_files(str(SAMPLE_FILE))
                page.wait_for_timeout(2000)  # 等待文件上传完成
            # page.get_by_role("button", name=" 点击上传").click()
            # page.get_by_role("button", name=" 点击上传").set_input_files("样例表.xlsx")
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="确 定").click()
            print(f"✅ 数据资源 {TEST_DATA['resource_name']} 挂载数据完成！")

            # 启用数据资源
            page.locator(".table-settings > .anticon > svg").first.click()
            page.get_by_role("button", name="启用").first.click()
            print(f"✅ 数据资源 {TEST_DATA['resource_name']} 创建并启用成功！")

            # 进入数据资源发布页面
            page.locator("div").filter(has_text=re.compile(r"^数据提供$")).click()
            page.get_by_role("listitem", name="数据资源发布").click()

            # 新增数据资源发布
            page.get_by_role("button", name=" 新增").click()
            # 资源定价环节
            # 选择数据资源编目
            page.locator("div").filter(has_text=re.compile(r"^请选择$")).nth(5).click()
            page.get_by_role("row").filter(has_text=TEST_DATA["resource_name"]).get_by_label("", exact=True).check()
            page.get_by_role("button", name="确 定").click()
            # 上传封面图
            # page.get_by_role("button", name="plus").click()
            if not COVER_IMAGE.exists():
                print(f"封面图文件不存在: {COVER_IMAGE}")
            else:
                page.locator("input[type='file']").set_input_files(str(COVER_IMAGE))
                page.wait_for_timeout(2000)  # 等待文件上传完成
            # page.get_by_role("button", name="plus").set_input_files("1.jpg")
            # 选择定价方式 设置产品价格
            page.get_by_role("combobox", name="* 定价方式").click()
            page.get_by_text("一口价").click()
            page.get_by_role("textbox", name="* 产品价格").click()
            page.get_by_role("textbox", name="* 产品价格").fill(TEST_DATA["price"])
            page.get_by_role("button", name="下一步").click()
            # 使用策略环节
            # 添加策略  调用次数限制3次
            page.get_by_role("combobox", name="选择策略").click()
            page.get_by_text("调用次数限制").click()
            page.get_by_role("button", name="添 加").click()
            page.get_by_role("spinbutton", name="请输入调用次数").click()
            page.get_by_role("spinbutton", name="请输入调用次数").fill("3")
            # 选择交付方式  数据服务
            page.get_by_role("combobox", name="* 交付方式").click()
            page.get_by_text("数据服务", exact=True).click()
            page.get_by_role("button", name="下一步").click()
            # 数据空间环节
            # 选择数据空间
            page.get_by_role("checkbox", name="尚数网可信数据空间").check()
            page.get_by_role("button", name="确 定").click()

            # 启用数据资源发布
            page.locator(".table-settings > .anticon > svg").first.click()
            page.get_by_role("button", name="启用").first.click()
            print(f"✅ 数据资源发布 {TEST_DATA['resource_name']} 创建并启用成功！")


            # 关闭浏览器
            context.close()
            browser.close()

            # 简单断言 证明跑完
            assert True
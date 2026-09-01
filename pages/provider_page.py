import re
from playwright.sync_api import Page
from pages.base_page import BasePage
from config import DELIVERY_METHOD, TEST_DATA, SAMPLE_FILE, COVER_IMAGE


class ProviderPage(BasePage):
    """提供方平台页面操作"""

    def login(self, username: str, password: str):
        """登录提供方平台"""
        self.goto("https://providernet.mayishangshu.cn:82/login?redirect=/home")
        self.get_by_role("textbox", name="请输入账号").click()
        self.get_by_role("textbox", name="请输入账号").fill(username)
        self.get_by_role("textbox", name="请输入密码").click()
        self.get_by_role("textbox", name="请输入密码").fill(password)
        self.get_by_role("button", name="登 录").click()
        print("✅ provider 登录成功！")

    def create_datasource(self):
        """创建 MySQL 数据源"""
        # 进入数据源管理页面
        self.page.get_by_role("listitem", name="数据源").click()
        self.page.locator(".icon-ym.icon-ym-nav-home-fill").click()
        self.page.locator("div").filter(has_text=re.compile(r"^数据资产管理$")).click()
        self.page.locator("div").filter(has_text=re.compile(r"^数据资产管理$")).click()
        self.page.get_by_role("listitem", name="数据源").click()

        # 新增数据源
        self.page.get_by_role("button", name="新增").click()
        self.page.get_by_role("textbox", name="* 数据源名称").click()
        self.page.get_by_role("textbox", name="* 数据源名称").fill(TEST_DATA["datasource_name"])
        self.page.get_by_role("combobox", name="* 数据源类型").click()
        self.page.locator("[id='711927340971634757']").get_by_text("MySQL", exact=True).click()
        self.page.get_by_role("textbox", name="* 地址 question-circle").fill("192.168.1.15")
        self.page.get_by_role("textbox", name="* 端口").fill("1966")
        self.page.get_by_role("textbox", name="* 数据库").fill("test")
        self.page.get_by_role("textbox", name="* 用户名").fill("root")
        self.page.get_by_role("textbox", name="* 密码").fill("2213")
        self.page.get_by_role("button", name="连接测试").click()
        self.wait_for_selector("text=数据库连接成功", timeout=10000)
        self.page.get_by_role("button", name="确 定").click()
        self.wait_for_selector("text=新建成功", timeout=10000)

        # 启用数据源
        self.page.locator(".table-settings > .anticon > svg").first.click()
        self.page.get_by_role("button", name="启用").first.click()
        self.wait_for_timeout(1000)
        print(f"✅ 数据源 {TEST_DATA['datasource_name']} 创建并启用成功！")

    def create_resource(self):
        """创建数据资源"""
        # 进入数据资源页面
        self.page.get_by_role("listitem", name="数据资源").click()

        # 新增数据资源
        self.page.get_by_role("button", name="新增").click()
        self.page.get_by_role("textbox", name="* 数据资源名称").fill(TEST_DATA["resource_name"])
        self.page.get_by_role("combobox", name="* 来源类型").click()
        self.page.get_by_text("原始取得").click()
        self.page.get_by_role("combobox", name="* 安全等级").click()
        self.page.get_by_text("公开数据，无安全保护要求").click()
        self.page.get_by_role("textbox", name="资源简介").fill("随便写的简介")
        self.page.locator("iframe[title='Rich Text Area']").content_frame.locator("html").click()
        self.page.locator("iframe[title='Rich Text Area']").content_frame.get_by_label("编辑区。按Alt+0键打开帮助。").fill("随便写的资源详情")
        self.page.get_by_role("button", name="确 定").click()
        self.page.locator(".table-settings > .anticon > svg").first.click()
        self.wait_for_timeout(3000)
        print(f"✅ 新增数据资源 {TEST_DATA['resource_name']} 完成！")

    def mount_data(self):
        """挂载数据"""
        self.page.get_by_role("button", name="挂载数据").first.click()
        self.wait_for_timeout(2000)
        self.page.locator("div").filter(has_text=re.compile(r"^请选择$")).nth(5).click()
        self.page.get_by_role("row", name=f"{TEST_DATA['datasource_name']} MySQL").get_by_label("", exact=True).check()
        self.page.get_by_label("选择数据").get_by_role("button", name="确 定").click()

        # 数据集配置
        self.page.get_by_role("textbox", name="数据集名称").fill(f"{TEST_DATA['resource_name']}_dataset")
        self.page.get_by_role("textbox", name="sql语句").fill("select * from desensitization")
        self.wait_for_timeout(2000)

        # 添加脱敏规则
        self.page.get_by_title("添加").nth(1).click()
        self.page.get_by_role("textbox", name="请输入").nth(4).fill("tel")
        self.page.locator("div").filter(has_text=re.compile(r"^请选择$")).nth(1).click()
        self.page.get_by_text("字符串").click()
        self.page.get_by_role("cell", name="请选择").click()
        self.page.get_by_text("掩码").click()
        self.page.get_by_role("textbox", name="请输入").nth(5).fill("2-9")
        self.page.get_by_role("button", name="数据测试").click()
        self.wait_for_timeout(2000)

        # 上传样例文件
        if SAMPLE_FILE.exists():
            self.page.locator("input[type='file']").set_input_files(str(SAMPLE_FILE))
            self.wait_for_timeout(2000)
        self.page.get_by_role("button", name="确 定").click()
        print(f"✅ 数据资源 {TEST_DATA['resource_name']} 挂载数据完成！")

    def publish_resource(self):
        """发布数据资源"""
        # 启用数据资源
        self.page.locator(".table-settings > .anticon > svg").first.click()
        self.page.get_by_role("button", name="启用").first.click()
        print(f"✅ 数据资源 {TEST_DATA['resource_name']} 创建并启用成功！")

        # 进入数据资源发布页面
        self.page.locator("div").filter(has_text=re.compile(r"^数据提供$")).click()
        self.page.get_by_role("listitem", name="数据资源发布").click()

        # 新增发布
        self.page.get_by_role("button", name="新增").click()
        self.page.locator("div").filter(has_text=re.compile(r"^请选择$")).nth(5).click()
        self.page.get_by_role("row").filter(has_text=TEST_DATA["resource_name"]).get_by_label("", exact=True).check()
        self.page.get_by_role("button", name="确 定").click()

        # 上传封面图
        if COVER_IMAGE.exists():
            self.page.locator("input[type='file']").set_input_files(str(COVER_IMAGE))
            self.wait_for_timeout(2000)

        # 定价
        self.page.get_by_role("combobox", name="* 定价方式").click()
        self.page.get_by_text("一口价").click()
        self.page.get_by_role("textbox", name="* 产品价格").fill(TEST_DATA["price"])
        self.page.get_by_role("button", name="下一步").click()

        # 使用策略
        self.page.get_by_role("combobox", name="选择策略").click()
        self.page.get_by_text("调用次数限制").click()
        self.page.get_by_role("button", name="添 加").click()
        self.page.get_by_role("spinbutton", name="请输入调用次数").fill("3")
        # 改为动态选择交付方式  config.py 中新增 DELIVERY_METHOD 配置项
        self.page.get_by_role("combobox", name="* 交付方式").click()
        # self.page.get_by_text("数据服务", exact=True).click()
        # self.page.get_by_text("安全沙盒", exact=True).click()
        # self.page.get_by_text("隐私计算", exact=True).click()
        self.page.get_by_text(DELIVERY_METHOD, exact=True).click()
        self.page.get_by_role("button", name="下一步").click()

        # 数据空间
        # self.page.get_by_role("checkbox", name="尚数网可信数据空间").check()
        self.page.get_by_role("checkbox", name=re.compile(r"可信数据空间")).check()
        self.page.get_by_role("button", name="确 定").click()

        # 启用发布
        self.page.locator(".table-settings > .anticon > svg").first.click()
        self.page.get_by_role("button", name="启用").first.click()
        print(f"✅ 数据资源发布 {TEST_DATA['resource_name']} 创建并启用成功！")

    def sign_order(self, order_no: str):
        """提供方签约"""
        self.page.locator("div").filter(has_text=re.compile(r"^数据提供$")).click()
        self.page.get_by_role("listitem", name="数据资源订单").click()
        self.wait_for_timeout(2000)
        self.page.get_by_role("row").filter(has_text=order_no).first.get_by_role("button", name="签约").click()
        self.page.get_by_role("radio", name="签约").check()
        self.page.get_by_role("button", name="确 定").click()
        print(f"✅ 提供方签约完成！订单号: {order_no}")

from playwright.sync_api import Page
from config import PLATFORMS

def login_platform(page: Page, platform_key: str):
    """
    通用的登录函数，使用示例：login_platform(page, "provider")，登录提供方连接器
    """
    info = PLATFORMS(platform_key)
    print(f"正在登录：{platform_key}")

    # 1.打开该平台网页
    page.goto(info["url"])

    # 2.输入账户密码并点击登录
    # 下放账号密码需替换成真实的
    # page.fill("#form_item_account", info["username"])
    # page.fill("#form_item_password", info["password"])
    # page.click("#button")

    # 3.等待登录成功后页面出现提示
    page.wait_for_selector("#welcome-message", timeout=5000)
    print(f"{platform_key} 登录成功！")
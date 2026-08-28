from playwright.sync_api import Page, sync_playwright


class BasePage:
    """页面对象基类，封装 Playwright 公共操作"""

    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        """打开页面"""
        self.page.goto(url)

    def click(self, locator, **kwargs):
        """点击元素"""
        self.page.locator(locator, **kwargs).click()

    def fill(self, locator, value: str, **kwargs):
        """填写输入框"""
        self.page.locator(locator, **kwargs).fill(value)

    def wait_for_selector(self, selector, timeout: int = 10000, **kwargs):
        """等待元素出现"""
        self.page.wait_for_selector(selector, timeout=timeout, **kwargs)

    def wait_for_timeout(self, milliseconds: int):
        """强制等待"""
        self.page.wait_for_timeout(milliseconds)

    def get_by_role(self, role: str, **kwargs):
        """根据角色获取元素"""
        return self.page.get_by_role(role, **kwargs)

    def locator(self, selector: str):
        """获取定位器"""
        return self.page.locator(selector)

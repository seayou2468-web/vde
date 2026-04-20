import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login?")
        await page.locator("#loginId").fill("e25040")
        await page.locator("#passwd").fill("Puze2968")
        await page.locator("#loginBtn").click()
        await page.wait_for_url("**/mypage")
        await page.locator("#serviceLinkLms").click()
        await page.wait_for_selector(".dataCell.kyoka")

        # Check course 8
        print("Taking screenshot of Course 8...")
        await page.evaluate("document.querySelectorAll('.dataCell.kyoka')[8].dispatchEvent(new MouseEvent('dblclick', {bubbles:true}))")
        await page.wait_for_selector(".rw.data2", timeout=30000)
        await page.screenshot(path="final_course_8.png", full_page=True)

        # Check course 22
        print("Taking screenshot of Course 22...")
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
        await page.wait_for_selector(".dataCell.kyoka")
        await page.evaluate("document.querySelectorAll('.dataCell.kyoka')[22].dispatchEvent(new MouseEvent('dblclick', {bubbles:true}))")
        await page.wait_for_selector(".rw.data2", timeout=30000)
        await page.screenshot(path="final_course_22.png", full_page=True)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

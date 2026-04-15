import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login?")
        await page.locator("#loginId").fill("e25040")
        await page.locator("#passwd").fill("Puze2968")
        await page.locator("#loginBtn").click()
        await page.wait_for_url("**/mypage")
        await page.locator("#serviceLinkLms").click()
        await page.wait_for_selector(".dataCell.kyoka", timeout=60000)

        # Take screenshot of course list
        await page.screenshot(path="debug_course_list.png")

        # Double click the first course
        print("Attempting double click on course 0...")
        await page.evaluate("document.querySelectorAll('.dataCell.kyoka')[0].dispatchEvent(new MouseEvent('dblclick', {bubbles:true}))")

        await asyncio.sleep(10)
        await page.screenshot(path="debug_after_dblclick.png")

        content = await page.content()
        with open("debug_after_dblclick.html", "w") as f:
            f.write(content)

        print("Check debug_after_dblclick.png and .html")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

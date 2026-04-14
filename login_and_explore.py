import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("Navigating to login page...")
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login?")

        await page.fill("#loginId", "e25040")
        await page.fill("#passwd", "Puze2968")

        print("Clicking login button...")
        await page.click("#loginBtn")

        await page.wait_for_selector("#serviceLinkLms")
        print("Logged in, clicking serviceLinkLms...")
        await page.click("#serviceLinkLms")

        # Wait for the next page to load
        await page.wait_for_timeout(10000)
        print("Current URL after clicking serviceLinkLms:", page.url)
        await page.screenshot(path="courses.png", full_page=True)

        content = await page.content()
        with open("courses.html", "w") as f:
            f.write(content)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

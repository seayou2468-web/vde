import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("Logging in...")
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login?")
        await page.fill("#loginId", "e25040")
        await page.fill("#passwd", "Puze2968")
        await page.click("#loginBtn")

        await page.wait_for_selector("#serviceLinkLms")
        await page.click("#serviceLinkLms")

        print("Waiting for LMS app to load...")
        # Wait for some time to let it stabilize
        await page.wait_for_timeout(10000)

        await page.screenshot(path="lms_debug.png", full_page=True)
        print("Screenshot saved as lms_debug.png")

        content = await page.content()
        with open("lms_debug.html", "w") as f:
            f.write(content)

        # Check all visible text
        text = await page.evaluate("() => document.body.innerText")
        print("Visible text preview:", text[:500])

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login?")
        await page.fill("#loginId", "e25040")
        await page.fill("#passwd", "Puze2968")
        await page.click("#loginBtn")

        await page.wait_for_selector("#serviceLinkLms")
        await page.click("#serviceLinkLms")

        # Wait for the courses to load. It might take time for the JS to fetch data.
        await page.wait_for_timeout(10000)

        # Look for course items
        # Usually they have some class like 'item' or 'course'
        items = await page.query_selector_all(".item")
        print(f"Found {len(items)} items with class '.item'")

        for i, item in enumerate(items):
            text = await item.inner_text()
            print(f"Item {i}: {text.replace('\n', ' ')}")

        # Try to find elements that might indicate completion
        completed = await page.query_selector_all(".done, .completed, .済")
        print(f"Found {len(completed)} completed items")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

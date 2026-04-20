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
        await page.wait_for_timeout(10000)

        course_cells = await page.query_selector_all(".dataCell.kyoka")
        print(f"Total course cells: {len(course_cells)}")
        for i, cell in enumerate(course_cells):
            text = await cell.inner_text()
            print(f"Course {i}: {text.replace('\n', ' ')}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

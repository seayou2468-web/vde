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
        await page.wait_for_timeout(5000)

        course_cells = await page.query_selector_all(".dataCell.kyoka")
        await course_cells[8].dblclick()
        await page.wait_for_timeout(5000)

        content = await page.content()
        with open("rows_debug.html", "w") as f:
            f.write(content)

        rows = await page.query_selector_all(".dataRow")
        print(f"Total rows: {len(rows)}")
        for i, row in enumerate(rows):
            html = await row.inner_html()
            print(f"Row {i} HTML snippet: {html[:100]}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

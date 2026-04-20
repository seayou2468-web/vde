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

        await page.wait_for_timeout(10000)

        # Click on "現国002-901 新編現代の国語"
        # I'll use a more generic way to find it
        course_cells = await page.query_selector_all(".dataCell.kyoka")
        target_cell = None
        for cell in course_cells:
            text = await cell.inner_text()
            if "新編現代の国語" in text:
                target_cell = cell
                break

        if target_cell:
            print("Target course found. Double clicking...")
            # Some UIs require double click or have specific hit areas
            await target_cell.dblclick()
            await page.wait_for_timeout(10000)
            await page.screenshot(path="nav_after_dblclick.png", full_page=True)

            # Check if any new elements appeared or if URL changed
            print("URL after dblclick:", page.url)

            # Let's try to find elements with class 'co lectureName' which I saw in courses.html
            lectures = await page.query_selector_all(".co.lectureName")
            print(f"Found {len(lectures)} lectureName elements")
            for i, l in enumerate(lectures):
                print(f"Lecture {i}: {await l.inner_text()}")
        else:
            print("Target course not found")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

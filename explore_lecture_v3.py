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

        # In the course list, if we click a row, does it open the lectures for that course?
        # Let's try to click exactly on the name element
        courses = await page.query_selector_all(".dataCell.kyoka")
        for course in courses:
            name_el = await course.query_selector(".name")
            name = await name_el.inner_text() if name_el else ""
            if "新編現代の国語" in name:
                print(f"Clicking on course name: {name}")
                await name_el.click()
                break

        await page.wait_for_timeout(10000)
        await page.screenshot(path="lectures_v3.png", full_page=True)

        content = await page.content()
        with open("lectures_v3.html", "w") as f:
            f.write(content)

        rows = await page.query_selector_all(".dataRow")
        print(f"Found {len(rows)} rows")
        for i, row in enumerate(rows):
            text = await row.inner_text()
            print(f"Row {i}: {text.replace('\n', ' ')}")

            # Check for play icon
            play_icon = await row.query_selector(".item.play")
            if play_icon:
                print(f"Found play icon in row {i}")
                # Check visibility
                is_visible = await play_icon.is_visible()
                print(f"Is play icon visible? {is_visible}")
                if is_visible:
                    await play_icon.click()
                    await page.wait_for_timeout(10000)
                    await page.screenshot(path="video_v3.png", full_page=True)
                    break

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

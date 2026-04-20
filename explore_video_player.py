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
        await page.wait_for_timeout(5000)

        course_cells = await page.query_selector_all(".dataCell.kyoka")
        target_cell = None
        for cell in course_cells:
            text = await cell.inner_text()
            if "新編現代の国語" in text:
                target_cell = cell
                break

        if target_cell:
            await target_cell.dblclick()
            await page.wait_for_timeout(5000)

            # Find a row that has a play button
            rows = await page.query_selector_all(".dataRow")
            for i, row in enumerate(rows):
                play_btn = await row.query_selector(".item.play")
                if play_icon := await row.query_selector(".item.play"):
                    print(f"Clicking play on row {i}")
                    await play_icon.click()
                    await page.wait_for_timeout(10000)

                    # We should be on the video player page now.
                    # Let's find the speed control and play button.
                    # According to the UI text: "✓標準", "×2.0" etc.
                    # Let's find all divs or spans containing "×2.0"

                    print("Looking for speed control...")
                    speed_20 = await page.get_by_text("×2.0").first
                    if await speed_20.is_visible():
                        print("Found 2.0x speed button. Clicking it...")
                        await speed_20.click()
                    else:
                        print("2.0x speed button not visible.")

                    # Find play button. Title was "再生/一時停止" or id "pictPlayerTool-play"
                    play_btn = await page.query_selector("#pictPlayerTool-play")
                    if play_btn:
                        print("Found play button. Clicking it...")
                        await play_btn.click()

                    # Check for video progress
                    # <span id="pictPlayerTool-duration1">0:00</span>/<span id="pictPlayerTool-duration2">0:00</span>
                    await page.wait_for_timeout(5000)
                    duration1 = await page.inner_text("#pictPlayerTool-duration1")
                    duration2 = await page.inner_text("#pictPlayerTool-duration2")
                    print(f"Progress: {duration1} / {duration2}")

                    await page.screenshot(path="video_playing.png", full_page=True)
                    break
        else:
            print("Course not found")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

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

        # Select "現国002-901 新編現代の国語" (Course 8)
        course_cells = await page.query_selector_all(".dataCell.kyoka")
        await course_cells[8].dblclick()
        await page.wait_for_timeout(5000)

        # Find a lecture to play
        rows = await page.query_selector_all(".rw.data2")
        for i, row in enumerate(rows):
            is_test = await row.query_selector(".play.test")
            complete = await row.get_attribute("data-complete")
            if not is_test and complete == "off":
                play_icon = await row.query_selector(".item.play.movie")
                if play_icon:
                    print(f"Playing video in row {i}...")
                    await play_icon.click()
                    await page.wait_for_timeout(5000)

                    # Try to set speed to 2.0x
                    # In my visible text earlier: "×2.0"
                    # It might be in a dropdown or a list
                    print("Setting speed to 2.0x...")
                    # Let's try to find the speed menu first if it exists
                    # Sometimes speed is hidden behind a button
                    speed_btn = await page.query_selector(".speed") # guessing
                    if speed_btn:
                        await speed_btn.click()

                    # Look for the element containing "×2.0"
                    target_speed = await page.get_by_text("×2.0").first
                    if await target_speed.is_visible():
                        await target_speed.click()
                        print("2.0x clicked.")
                    else:
                        print("2.0x NOT visible. Maybe it needs a click on a speed menu?")
                        # Let's take a screenshot to see the player controls
                        await page.screenshot(path="player_controls.png")

                    # Click play
                    play_btn = await page.query_selector("#pictPlayerTool-play")
                    if play_btn:
                        await play_btn.click()
                        print("Play clicked.")

                    await page.wait_for_timeout(5000)
                    # Check if duration changed
                    d1 = await page.inner_text("#pictPlayerTool-duration1")
                    print(f"Duration: {d1}")

                    # Now test the "Back" button
                    print("Testing Back button...")
                    back_btn = await page.query_selector("#pictPlayerTool-back")
                    if back_btn:
                        await back_btn.click()
                        await page.wait_for_timeout(5000)
                        print("Back clicked. URL:", page.url)
                        if await page.is_visible(".rw.data2"):
                            print("Back to lecture list successful.")
                    break

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

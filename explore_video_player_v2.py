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

        # Course 8: 現国002-901 新編現代の国語
        course_cells = await page.query_selector_all(".dataCell.kyoka")
        target_cell = course_cells[8]
        print(f"Clicking course: {await target_cell.inner_text()}")
        await target_cell.dblclick()
        await page.wait_for_timeout(5000)

        # Find a lecture that is not finished
        rows = await page.query_selector_all(".dataRow")
        print(f"Found {len(rows)} rows")
        for i, row in enumerate(rows):
            mark_el = await row.query_selector(".co.mark")
            mark_text = await mark_el.inner_text() if mark_el else ""
            if "視聴済" not in mark_text:
                play_icon = await row.query_selector(".item.play")
                if play_icon:
                    print(f"Row {i} is NOT finished. Clicking play.")
                    await play_icon.click()
                    await page.wait_for_timeout(10000)

                    await page.screenshot(path="player_check.png", full_page=True)

                    # Try to set speed to 2.0x
                    # In the screenshot/content, look for speed buttons
                    speed_buttons = await page.query_selector_all("div, span")
                    for btn in speed_buttons:
                        btn_text = await btn.inner_text()
                        if "2.0" in btn_text:
                            print(f"Found speed button: {btn_text}. Clicking it.")
                            await btn.click()
                            break

                    # Click play
                    play_btn = await page.query_selector("#pictPlayerTool-play")
                    if play_btn:
                        print("Clicking play button...")
                        await play_btn.click()

                    # Monitor progress
                    for _ in range(5):
                        await page.wait_for_timeout(5000)
                        d1 = await page.inner_text("#pictPlayerTool-duration1")
                        d2 = await page.inner_text("#pictPlayerTool-duration2")
                        print(f"Current progress: {d1} / {d2}")
                        if d1 == d2 and d1 != "0:00":
                            print("Finished!")
                            break
                    break

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

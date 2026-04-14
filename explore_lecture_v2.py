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

        # We are at the course list
        courses = await page.query_selector_all(".dataRow[data-group='on']")
        print(f"Found {len(courses)} course rows")

        # Let's try to find a course that has some progress but not 100% or just pick one
        # "現国002-901 新編現代の国語" was mentioned.
        target_course = None
        for course in courses:
            text = await course.inner_text()
            if "新編現代の国語" in text:
                target_course = course
                break

        if not target_course:
            target_course = courses[0]

        print(f"Clicking course: {await target_course.inner_text()}")
        # Click the row
        await target_course.click()

        # Wait for transition to lecture list
        await page.wait_for_timeout(5000)
        await page.screenshot(path="after_course_click.png", full_page=True)

        # Look for chapters or lessons
        # Usually it's a table with .dataRow
        rows = await page.query_selector_all(".dataRow")
        print(f"Found {len(rows)} rows after clicking course")

        for i, row in enumerate(rows):
            text = await row.inner_text()
            print(f"Row {i}: {text.replace('\n', ' ')}")

            # Look for a play button or something that indicates a video
            # From previous grep: <div class="item play">動画視聴</div>
            play_btn = await row.query_selector(".item.play")
            if play_btn:
                print(f"Found play button in Row {i}. Clicking it.")
                # Ensure it's visible and clickable
                await play_btn.scroll_into_view_if_needed()
                await play_btn.click()

                await page.wait_for_timeout(10000)
                await page.screenshot(path="video_page.png", full_page=True)

                # Check for video tag or player controls
                video_exists = await page.query_selector("video")
                print(f"Video tag exists: {video_exists is not None}")

                # Check for speed controls
                # In previous visible text I saw: ✓標準 ×1.5 ×1.6 ... ×2.0
                speed_controls = await page.query_selector_all(".speed") # guessing class
                print(f"Found {len(speed_controls)} speed controls")

                content = await page.content()
                with open("video_page.html", "w") as f:
                    f.write(content)
                break

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

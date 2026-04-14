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

        courses = await page.query_selector_all(".dataCell.kyoka")
        print(f"Found {len(courses)} courses")

        if courses:
            name_el = await courses[0].query_selector('.name')
            name = await name_el.inner_text() if name_el else "Unknown"
            print(f"Clicking course: {name}")
            await courses[0].click()
            await page.wait_for_timeout(5000)

            await page.screenshot(path="lecture_list.png", full_page=True)

            # Now we should be in the lecture list for that course.
            lectures = await page.query_selector_all(".dataRow")
            print(f"Found {len(lectures)} rows in lecture list")

            for i, lecture in enumerate(lectures):
                text = await lecture.inner_text()
                # Check for "済" mark in the row
                mark_el = await lecture.query_selector(".co.mark")
                mark_text = await mark_el.inner_text() if mark_el else ""

                if "済" not in mark_text:
                    print(f"Lecture {i} is NOT finished. Text: {text[:50].replace('\n', ' ')}")

                    play_btn = await lecture.query_selector(".co.play")
                    if play_btn:
                        print(f"Clicking play button for lecture {i}")
                        await play_btn.click()
                        await page.wait_for_timeout(10000)

                        await page.screenshot(path="video_player.png", full_page=True)

                        content = await page.content()
                        with open("video_player.html", "w") as f:
                            f.write(content)
                        break
                else:
                    print(f"Lecture {i} is already finished.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

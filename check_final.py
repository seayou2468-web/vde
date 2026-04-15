import asyncio
import sys
import os
from playwright.async_api import async_playwright

async def main():
    login_id = "e25040"
    password = "Puze2968"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("Logging in for final check...")
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login?")
        await page.locator("#loginId").fill(login_id)
        await page.locator("#passwd").fill(password)
        await page.locator("#loginBtn").click()
        await page.wait_for_url("**/oslms/mypage")

        lms = page.locator("#serviceLinkLms")
        if await lms.count() > 0: await lms.click()

        await page.wait_for_selector(".dataCell.kyoka")
        courses_count = await page.locator(".dataCell.kyoka").count()
        print(f"Total courses: {courses_count}")

        total_unfinished = 0
        for i in range(courses_count):
            # Refresh and Enter
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await page.wait_for_selector(".dataCell.kyoka")

            course_name = await page.locator(".dataCell.kyoka .name").nth(i).inner_text()
            await page.evaluate(f"document.querySelectorAll('.dataCell.kyoka')[{i}].dispatchEvent(new MouseEvent('dblclick', {{bubbles:true}}))")

            try:
                await page.wait_for_selector(".rw.data2", timeout=10000)
                unfinished = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('.rw.data2'))
                        .filter(r => r.getAttribute('data-complete') === 'off' && !r.querySelector('.play.test') && r.querySelector('.item.play.movie'))
                        .length;
                }''')
                print(f"  Course {i} ({course_name}): {unfinished} unfinished.")
                total_unfinished += unfinished
            except:
                print(f"  Course {i} ({course_name}): No rows or load error.")

        print(f"\nTOTAL UNFINISHED VIDEOS: {total_unfinished}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

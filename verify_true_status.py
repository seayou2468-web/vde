import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0")
        page = await context.new_page()

        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login?")
        await page.locator("#loginId").fill("e25040")
        await page.locator("#passwd").fill("Puze2968")
        await page.locator("#loginBtn").click()
        await page.wait_for_url("**/oslms/mypage")
        await page.locator("#serviceLinkLms").click()
        await page.wait_for_selector(".dataCell.kyoka")

        counts = await page.locator(".dataCell.kyoka").count()
        print(f"Total courses found: {counts}")

        grand_total = 0
        for i in range(counts):
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await page.wait_for_selector(".dataCell.kyoka")

            # Use JS to double click
            await page.evaluate(f"document.querySelectorAll('.dataCell.kyoka')[{i}].dispatchEvent(new MouseEvent('dblclick', {{bubbles:true}}))")

            # Wait for rows with a long timeout
            try:
                await page.wait_for_selector(".rw.data2", timeout=20000)
                # Count using JS
                unfinished = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('.rw.data2'))
                        .filter(r => r.getAttribute('data-complete') === 'off' && !r.querySelector('.play.test') && r.querySelector('.item.play.movie'))
                        .length;
                }''')
                print(f"Course {i}: {unfinished} unfinished videos.")
                grand_total += unfinished
            except:
                print(f"Course {i}: Could not load rows.")

        print(f"\nGRAND TOTAL UNFINISHED: {grand_total}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

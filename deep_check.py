import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login?")
        await page.locator("#loginId").fill("e25040")
        await page.locator("#passwd").fill("Puze2968")
        await page.locator("#loginBtn").click()
        await page.wait_for_url("**/mypage")
        await page.locator("#serviceLinkLms").click()
        await page.wait_for_selector(".dataCell.kyoka", timeout=60000)

        courses_count = await page.locator(".dataCell.kyoka").count()
        print(f"Total courses: {courses_count}")

        for i in range(courses_count):
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await page.wait_for_selector(".dataCell.kyoka")

            name = await page.locator(".dataCell.kyoka .name").nth(i).inner_text()
            print(f"Checking {name}...")

            # Enter
            await page.evaluate(f"document.querySelectorAll('.dataCell.kyoka')[{i}].dispatchEvent(new MouseEvent('dblclick', {{bubbles:true}}))")

            try:
                # Wait for any data row or specific ID
                await page.wait_for_selector("[id^='lsi'], .rw.data2", timeout=30000)
                unfinished = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('.rw.data2, [id^="lsi"]'))
                        .filter(r => r.getAttribute('data-complete') === 'off' && !r.querySelector('.play.test') && (r.querySelector('.item.play.movie') || r.querySelector('.play.movie')))
                        .length;
                }''')
                if unfinished > 0:
                    print(f"  !!! Course {i} has {unfinished} unfinished videos.")
                else:
                    print(f"  Clean.")
            except:
                print(f"  Could not load rows for {name}.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

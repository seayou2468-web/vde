import asyncio
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
        await page.wait_for_url("**/mypage")
        await page.locator("#serviceLinkLms").click()
        await page.wait_for_selector(".dataCell.kyoka")

        counts = await page.locator(".dataCell.kyoka").count()
        print(f"Total courses: {counts}")

        for i in range(counts):
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await page.wait_for_selector(".dataCell.kyoka")

            name = await page.locator(".dataCell.kyoka .name").nth(i).inner_text()
            print(f"Checking {name}...")

            await page.evaluate(f"document.querySelectorAll('.dataCell.kyoka')[{i}].dispatchEvent(new MouseEvent('dblclick', {{bubbles:true}}))")

            # Wait for list or no rows
            try:
                await page.wait_for_selector(".rw.data2", timeout=20000)
                unfinished = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('.rw.data2'))
                        .filter(r => r.getAttribute('data-complete') === 'off' && !r.querySelector('.play.test') && r.querySelector('.item.play.movie'))
                        .map(r => r.id);
                }''')
                if unfinished:
                    print(f"  !!! Found {len(unfinished)} unfinished in {name}: {unfinished}")
                else:
                    print(f"  Clean.")
            except:
                print(f"  No lectures found or load timeout.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

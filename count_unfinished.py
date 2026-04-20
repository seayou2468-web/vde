import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login?")
        await page.locator("#loginId").fill("e25040")
        await page.locator("#passwd").fill("Puze2968")
        await page.locator("#loginBtn").click()
        await page.wait_for_url("**/mypage")
        await page.locator("#serviceLinkLms").click()
        await page.wait_for_selector(".dataCell.kyoka", timeout=60000)

        counts = await page.locator(".dataCell.kyoka").count()
        total = 0
        for i in range(counts):
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await page.wait_for_selector(".dataCell.kyoka")
            await page.evaluate(f"document.querySelectorAll('.dataCell.kyoka')[{i}].dispatchEvent(new MouseEvent('dblclick', {{bubbles:true}}))")
            try:
                await page.wait_for_selector("[id^='lsi'], .rw.data2", timeout=15000)
                unfinished = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('.rw.data2, [id^="lsi"]'))
                        .filter(r => r.getAttribute('data-complete') === 'off' && !r.querySelector('.play.test') && (r.querySelector('.item.play.movie') || r.querySelector('.play.movie')))
                        .length;
                }''')
                if unfinished > 0:
                    name = await page.evaluate(f"document.querySelectorAll('.dataCell.kyoka')[{i}].querySelector('.name').innerText")
                    print(f"Course {i} ({name}): {unfinished} unfinished.")
                total += unfinished
            except:
                pass
        print(f"TOTAL UNFINISHED: {total}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

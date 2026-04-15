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

        print("Entering Course 22...")
        await page.evaluate("document.querySelectorAll('.dataCell.kyoka')[22].dispatchEvent(new MouseEvent('dblclick', {bubbles:true}))")

        await page.wait_for_selector(".rw.data2", timeout=60000)
        unfinished = await page.evaluate('''() => {
            const rows = Array.from(document.querySelectorAll('.rw.data2'));
            return rows.filter(r => r.getAttribute('data-complete') === 'off' && !r.querySelector('.play.test') && r.querySelector('.item.play.movie')).length;
        }''')
        print(f"Course 22 unfinished videos: {unfinished}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

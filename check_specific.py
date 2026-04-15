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
        await page.wait_for_selector(".dataCell.kyoka")

        # Check course 22 specifically
        i = 22
        print(f"Checking course {i}...")
        await page.evaluate(f"document.querySelectorAll('.dataCell.kyoka')[{i}].dispatchEvent(new MouseEvent('dblclick', {{bubbles:true}}))")
        await page.wait_for_selector(".rw.data2", timeout=30000)

        unfinished = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('.rw.data2'))
                .filter(r => r.getAttribute('data-complete') === 'off' && !r.querySelector('.play.test') && r.querySelector('.item.play.movie'))
                .length;
        }''')
        print(f"Course {i} unfinished: {unfinished}")

        # Check course 8 (modern japanese)
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
        await page.wait_for_selector(".dataCell.kyoka")
        await page.evaluate(f"document.querySelectorAll('.dataCell.kyoka')[8].dispatchEvent(new MouseEvent('dblclick', {{bubbles:true}}))")
        await page.wait_for_selector(".rw.data2", timeout=30000)
        unfinished_8 = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('.rw.data2'))
                .filter(r => r.getAttribute('data-complete') === 'off' && !r.querySelector('.play.test') && r.querySelector('.item.play.movie'))
                .length;
        }''')
        print(f"Course 8 unfinished: {unfinished_8}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

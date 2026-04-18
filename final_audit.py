import asyncio
from playwright.async_api import async_playwright

async def audit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await page.fill('#loginId', "e25040")
        await page.fill('#passwd', "Puze2968")
        await page.click('#loginBtn')
        await asyncio.sleep(10)
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
        await asyncio.sleep(15)
        
        subs = await page.query_selector_all('.dataRow')
        count = len(subs)
        print(f"Total Subjects found on dashboard: {count}")
        
        for i in range(count):
            # Refresh subs list
            subs = await page.query_selector_all('.dataRow')
            s = subs[i]
            name = await (await s.query_selector('.name')).inner_text()
            
            # Click subject
            await page.evaluate("el => el.click()", s)
            await asyncio.sleep(10)
            
            # Remove overlays
            await page.evaluate("document.querySelectorAll('.WafDialogModalCover, .WafDialogWindow').forEach(o => o.remove())")
            
            # Expand all units
            expandables = await page.query_selector_all('.rw.data1.close, .expandable.contract')
            for exp in expandables:
                await page.evaluate("el => el.click()", exp)
                await asyncio.sleep(1)
            
            await asyncio.sleep(3)
            lecs = await page.query_selector_all('.rw.data2')
            total = len(lecs)
            done = 0
            tests = 0
            for l in lecs:
                cls = await l.get_attribute('class') or ""
                if 'test' in cls:
                    tests += 1
                    continue
                if await l.get_attribute('data-complete') == 'on':
                    done += 1
            
            actual_total = total - tests
            print(f"[{i:02}] {name}: {done}/{actual_total} (Tests: {tests})")
            
            # Back to dashboard
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await asyncio.sleep(10)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(audit())

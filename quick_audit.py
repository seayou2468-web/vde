import asyncio
from playwright.async_api import async_playwright

async def run():
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
        for i, s in enumerate(subs):
            name_el = await s.query_selector('.name')
            name = await name_el.inner_text() if name_el else "???"
            # Enter subject to see true lecture progress
            await page.evaluate("el => el.click()", s)
            await asyncio.sleep(10)
            
            lecs = await page.query_selector_all('.rw.data2')
            total = len(lecs)
            done = 0
            for l in lecs:
                if await l.get_attribute('data-complete') == 'on':
                    done += 1
            
            print(f"[{i}] {name}: {done}/{total} ({(done/total*100) if total > 0 else 0:.1f}%)")
            
            # Go back
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await asyncio.sleep(10)
            subs = await page.query_selector_all('.dataRow')
            
        await browser.close()

asyncio.run(run())

import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await page.fill('#loginId', "e25040")
        await page.fill('#passwd', "Puze2968")
        await page.click('#loginBtn')
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(5)
        await page.click("text=東京書籍 インターネット講座")
        await asyncio.sleep(5)
        
        subs = await page.query_selector_all('.dataRow[data-group="on"]')
        print(f"Total Subjects: {len(subs)}")
        for i in range(len(subs)):
            subs = await page.query_selector_all('.dataRow[data-group="on"]')
            sub = subs[i]
            name = await (await sub.query_selector('.name')).inner_text()
            await sub.click()
            await asyncio.sleep(2)
            lecs = await page.query_selector_all('.rw.data2')
            total = len(lecs)
            done = 0
            for l in lecs:
                if await l.get_attribute('data-complete') == 'on':
                    done += 1
            print(f"{name}: {done}/{total}")
            await page.evaluate("document.getElementById('lectureBack').click()")
            await asyncio.sleep(1)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

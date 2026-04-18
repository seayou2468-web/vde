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
        
        # Take a snapshot of the list
        await page.screenshot(path="screenshots/dashboard_v.png")
        
        subs = await page.query_selector_all('.dataRow')
        print(f"Total Subjects: {len(subs)}")
        for i, s in enumerate(subs):
            name_el = await s.query_selector('.name')
            comp_el = await s.query_selector('.comp')
            name = await name_el.inner_text() if name_el else "Unknown"
            comp = await comp_el.inner_text() if comp_el else "N/A"
            print(f"[{i}] {name}: {comp}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

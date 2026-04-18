import asyncio
import sys
sys.path.append('/home/jules/self_created_tools')
from human_sim import HumanSim
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Login...")
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await page.fill('#loginId', "e25040")
        await page.fill('#passwd', "Puze2968")
        await page.click('#loginBtn')
        await asyncio.sleep(5)
        print("Clicking Course...")
        await page.click("text=東京書籍 インターネット講座")
        await asyncio.sleep(10)
        await page.screenshot(path="screenshots/subs_debug.png")
        
        subs = await page.query_selector_all('.dataRow')
        print(f"Found {len(subs)} dataRow elements.")
        for s in subs:
            group = await s.get_attribute('data-group')
            name_el = await s.query_selector('.name')
            name = await name_el.inner_text() if name_el else "NO NAME"
            comp_el = await s.query_selector('.comp')
            comp = await comp_el.inner_text() if comp_el else "NO COMP"
            print(f"Row: group={group}, name={name}, comp={comp}")
            
        await browser.close()

asyncio.run(run())

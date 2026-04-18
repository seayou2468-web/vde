import asyncio
import sys
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
        
        rows = await page.query_selector_all('.dataRow')
        # Science and Human Life is usually index 15
        sub = rows[15]
        await sub.click()
        await asyncio.sleep(15)
        
        lec = await page.query_selector('#lsi75658')
        if lec:
            comp = await lec.get_attribute('data-complete')
            print(f"LSI75658 status: {comp}")
            await lec.screenshot(path="screenshots/check_lsi75658.png")
        else:
            print("Lecture not found.")
            
        await browser.close()

asyncio.run(run())

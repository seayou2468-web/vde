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
        sub = rows[8]
        await sub.click()
        await asyncio.sleep(10)
        
        lecs = await page.query_selector_all('.rw.data2')
        for i, l in enumerate(lecs[:20]):
            lid = await l.get_attribute('id')
            comp = await l.get_attribute('data-complete')
            cls = await l.get_attribute('class')
            text = await l.inner_text()
            print(f"[{i}] ID: {lid} | Comp: {comp} | Class: {cls} | Text: {text.strip().replace('\n', ' ')}")
            
        await browser.close()

asyncio.run(run())

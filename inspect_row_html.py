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
        await asyncio.sleep(5)
        await page.click("text=東京書籍 インターネット講座")
        await asyncio.sleep(5)
        await page.click('.dataRow >> nth=8')
        await asyncio.sleep(5)
        
        row = await page.wait_for_selector('.rw.data2[data-complete="off"]')
        html = await row.inner_html()
        print(html)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
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
        
        # Take screenshot of the first incomplete lecture row
        row = await page.wait_for_selector('.rw.data2[data-complete="off"]')
        await row.scroll_into_view_if_needed()
        await asyncio.sleep(1)
        await row.screenshot(path="screenshots/s9_row_visual.png")
        print(f"Captured row: {row}")
        
        # Capture the whole list
        await page.screenshot(path="screenshots/s9_list_visual.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

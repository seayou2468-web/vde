import asyncio
import sys
import os
sys.path.append('/home/jules/self_created_tools')
from human_sim import human_move_and_click, human_type
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await human_type(page, 'input#loginId', "e25040")
        await human_type(page, 'input#passwd', "Puze2968")
        await human_move_and_click(page, 'input#loginBtn')
        await asyncio.sleep(5)
        
        await page.click("text=東京書籍 インターネット講座")
        await asyncio.sleep(5)
        
        # Subject 1
        await human_move_and_click(page, '.dataRow[data-group="on"] >> nth=0')
        await asyncio.sleep(3)
        
        target = await page.query_selector('#contentsPropertyList .rw.data2 >> nth=0')
        tid = await target.get_attribute('id')
        print(f"Double clicking {tid}...")
        
        box = await target.bounding_box()
        tx, ty = box['x'] + box['width']/2, box['y'] + box['height']/2
        await page.mouse.move(tx, ty)
        await page.mouse.click(tx, ty, click_count=2)
        
        await asyncio.sleep(5)
        if await page.is_visible('#mPlayer:not(.hidden)'):
            print("SUCCESS with double click!")
        else:
            print("FAILED with double click.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

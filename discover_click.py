import asyncio
import sys
import os
import random
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
        
        # S25
        await human_move_and_click(page, '.dataRow[data-group="on"] >> nth=24')
        await asyncio.sleep(5)
        
        tid = 'lsi63199' # L6
        target = await page.wait_for_selector(f'#{tid}', state="attached")
        await page.evaluate(f"document.getElementById('{tid}').scrollIntoView({{block: 'center'}})")
        await asyncio.sleep(1)
        
        # Get all clickable sub-elements
        elements = await target.query_selector_all('div')
        print(f"Found {len(elements)} div sub-elements in {tid}")
        
        for i, el in enumerate(elements):
            # Check if it has any text or icon
            cls = await el.get_attribute('class') or ""
            txt = (await el.inner_text()).strip()
            if "icon" in cls or "lectureName" in cls or "ce" in cls:
                print(f"Trying sub-element {i}: class='{cls}', text='{txt}'")
                box = await el.bounding_box()
                if box and box['width'] > 0:
                    tx, ty = box['x'] + box['width']/2, box['y'] + box['height']/2
                    await page.mouse.move(tx, ty, steps=10)
                    await asyncio.sleep(0.5)
                    await page.mouse.click(tx, ty)
                    await asyncio.sleep(3)
                    
                    if await page.is_visible('#mPlayer:not(.hidden)') or await page.is_visible('#mPictPlayer:not(.hidden)'):
                        print(f"SUCCESS with sub-element {i}!")
                        return
                    else:
                        # If we moved away (unlikely if player is hidden), go back
                        if not await page.is_visible(f'#{tid}'):
                             # Try to find a back button
                             for b in ['#player1Back', '#test1Back', '#pictPlayerTool-back', '#lectureBack']:
                                 if await page.is_visible(b):
                                     await page.click(b)
                                     await asyncio.sleep(2)
                                     break
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

import asyncio
import sys
import os
sys.path.append('/home/jules/self_created_tools')
from human_sim import human_move_and_click, human_type
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Using a larger viewport to ensure everything fits better
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        print("Logging in...")
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await human_type(page, 'input#loginId', "e25040")
        await human_type(page, 'input#passwd', "Puze2968")
        await human_move_and_click(page, 'input#loginBtn')
        await asyncio.sleep(5)
        
        print("Entering Internet Course...")
        # Try to find the link by text and click human-like
        await human_move_and_click(page, "text=東京書籍 インターネット講座")
        await asyncio.sleep(5)
        
        # S25
        print("Clicking Subject 25...")
        await human_move_and_click(page, '.dataRow[data-group="on"] >> nth=24')
        await asyncio.sleep(5)
        
        # Find L6 (incomplete)
        target_name = "6"
        lectures = await page.query_selector_all('#contentsPropertyList .rw.data2')
        target = None
        for l in lectures:
            name_el = await l.query_selector('.lectureName')
            name = await name_el.inner_text() if name_el else ""
            if name.strip() == target_name:
                target = l
                break
        
        if target:
            tid = await target.get_attribute('id')
            print(f"Targeting Lecture {target_name} ({tid})")
            
            # Hover first
            box = await target.bounding_box()
            await page.mouse.move(box['x'] + 10, box['y'] + 10, steps=10)
            await asyncio.sleep(1)
            
            # Try clicking the 'Play' cell specifically
            play_cell = await target.query_selector('.play.movie')
            print("Clicking Play cell...")
            await human_move_and_click(page, play_cell)
            await asyncio.sleep(10)
            
            await page.screenshot(path="screenshots/s25_manual_attempt.png")
            
            if await page.is_visible('#mPlayer:not(.hidden)'):
                print("SUCCESS: Player opened!")
            elif await page.is_visible('#mPictPlayer:not(.hidden)'):
                print("SUCCESS: PictPlayer opened!")
            else:
                print("FAILED: Player still hidden.")
        else:
            print("Target lecture not found.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

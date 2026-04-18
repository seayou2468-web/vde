import asyncio
import sys
import os
sys.path.append('/home/jules/self_created_tools')
from human_sim import human_move_and_click, human_type
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await human_type(page, 'input#loginId', "e25040")
        await human_type(page, 'input#passwd', "Puze2968")
        await human_move_and_click(page, 'input#loginBtn')
        await asyncio.sleep(5)
        
        await page.click("text=東京書籍 インターネット講座")
        await asyncio.sleep(5)
        
        # Subject 9
        await human_move_and_click(page, '.dataRow[data-group="on"] >> nth=8')
        await asyncio.sleep(5)
        
        # Find L98 (lsi74465)
        target = await page.wait_for_selector('#lsi74465', state="attached")
        await page.evaluate("el => el.scrollIntoView({block: 'center'})", target)
        await asyncio.sleep(2)
        
        # Click the play cell specifically
        play_cell = await target.query_selector('.play.movie')
        print("Clicking play cell of L98...")
        
        # Use a more direct but still simulated click
        box = await page.evaluate("el => { const r = el.getBoundingClientRect(); return {x: r.left, y: r.top, width: r.width, height: r.height}; }", play_cell)
        tx = box['x'] + box['width']/2
        ty = box['y'] + box['height']/2
        await page.mouse.move(tx, ty, steps=10)
        await asyncio.sleep(0.5)
        await page.mouse.click(tx, ty)
        
        await asyncio.sleep(10)
        
        if await page.is_visible('#mPlayer:not(.hidden)'):
            print("SUCCESS: Player opened!")
        else:
            print("FAILED. Player still hidden.")
            await page.screenshot(path="screenshots/targeted_fail.png")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

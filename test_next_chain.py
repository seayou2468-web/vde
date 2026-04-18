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
        
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))

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
        
        # Click the first lecture (which is complete)
        first_lecture = await page.query_selector('#contentsPropertyList .rw.data2 >> nth=0')
        print("Clicking first lecture...")
        await human_move_and_click(page, first_lecture)
        await asyncio.sleep(5)
        
        if await page.is_visible('#mPlayer:not(.hidden)'):
            print("SUCCESS: Player opened!")
            # Try to click Next immediately to see if it works
            btn = '#player2Next' if await page.is_visible('#player2Next') else '#player1Next'
            print(f"Clicking Next ({btn})...")
            await human_move_and_click(page, btn)
            await asyncio.sleep(5)
            # Check if we are in the next lecture
            # We can check the title or something
            print("After Next click.")
            await page.screenshot(path="screenshots/next_chain_check.png")
        else:
            print("FAILED: Could not even open the first lecture.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

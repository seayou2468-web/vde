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
        
        # S9
        await human_move_and_click(page, '.dataRow[data-group="on"] >> nth=8')
        await asyncio.sleep(3)
        
        # Click target
        await human_move_and_click(page, '#lsi74465')
        await asyncio.sleep(5)
        
        # If player not visible, try to click again or use JS
        if await page.is_visible('#mPlayer.hidden'):
            print("Player still hidden. Trying JS click...")
            await page.evaluate("document.getElementById('lsi74465').click()")
            await asyncio.sleep(5)
            
        await page.screenshot(path="screenshots/s9_force_check.png")
        
        if await page.is_visible('#mPlayer:not(.hidden)'):
            print("SUCCESS: Player visible!")
        else:
            print("FAILED: Player still hidden.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

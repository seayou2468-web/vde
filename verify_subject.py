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
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(5)
        
        await page.click("text=東京書籍 インターネット講座")
        await asyncio.sleep(5)
        
        # Click the first subject
        await human_move_and_click(page, '.dataRow[data-group="on"] >> nth=0')
        await asyncio.sleep(3)
        
        await page.screenshot(path="screenshots/verify_subject_0.png", full_page=True)
        
        # Go back and check a later one, say 24 (Music)
        await human_move_and_click(page, '#lectureBack')
        await asyncio.sleep(2)
        await human_move_and_click(page, '.dataRow[data-group="on"] >> nth=23')
        await asyncio.sleep(3)
        await page.screenshot(path="screenshots/verify_subject_23.png", full_page=True)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

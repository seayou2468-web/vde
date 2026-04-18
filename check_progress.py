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
        
        print("Logging in...")
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await human_type(page, 'input#loginId', "e25040")
        await human_type(page, 'input#passwd', "Puze2968")
        await human_move_and_click(page, 'input#loginBtn')
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(5)
        
        print("Entering internet course...")
        await page.click("text=東京書籍 インターネット講座")
        await asyncio.sleep(5)
        
        subjects = await page.query_selector_all('.dataRow[data-group="on"]')
        print(f"Found {len(subjects)} subjects.")
        
        for i, subject in enumerate(subjects):
            name = await (await subject.query_selector('.name')).inner_text()
            # Try to get progress. It's a canvas, so maybe we can't get text easily, 
            # but let's see if there's any data attribute or hidden text.
            # Wait, there was "視聴達成率" (Viewing achievement rate) in the header.
            # Maybe the row has it?
            print(f"Subject {i+1}: {name}")
            
        await page.screenshot(path="screenshots/subject_list_check.png", full_page=True)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

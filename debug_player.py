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
        
        lectures = await page.query_selector_all('#contentsPropertyList .rw.data2')
        target = None
        for lecture in lectures:
            comp = await lecture.get_attribute('data-complete')
            playable = await lecture.get_attribute('data-playable')
            if comp != 'on' and playable == 'on':
                target = lecture
                break
        
        if target:
            name = await (await target.query_selector('.lectureName')).inner_text()
            print(f"Clicking lecture: {name}")
            await human_move_and_click(page, target)
            await asyncio.sleep(10)
            
            await page.screenshot(path="screenshots/debug_player_s9.png")
            
            # Dump HTML of the player page
            content = await page.content()
            with open("debug_player_s9.html", "w") as f:
                f.write(content)
            print("Debug info saved.")
        else:
            print("No incomplete video found in S9.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

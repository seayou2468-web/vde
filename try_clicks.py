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
        
        # S9
        await human_move_and_click(page, '.dataRow[data-group="on"] >> nth=8')
        await asyncio.sleep(5)
        
        target_id = 'lsi74465'
        target = await page.wait_for_selector(f'#{target_id}')
        
        targets = [
            f'#{target_id}',
            f'#{target_id} .lectureName',
            f'#{target_id} .play.movie',
            f'#{target_id} .play.movie .icon'
        ]
        
        for t in targets:
            print(f"Trying click on: {t}")
            try:
                await page.evaluate(f"document.getElementById('{target_id}').scrollIntoView()")
                await asyncio.sleep(1)
                await human_move_and_click(page, t)
                await asyncio.sleep(5)
                if await page.is_visible('#mPlayer:not(.hidden)'):
                    print(f"SUCCESS with {t}")
                    break
                else:
                    print(f"Failed with {t}")
                    # If we are in another page (like a test or info), go back
                    for b in ['#player1Back', '#test1Back', '#info1Back']:
                        if await page.is_visible(b):
                            await human_move_and_click(page, b)
                            await asyncio.sleep(2)
            except Exception as e:
                print(f"Error with {t}: {e}")
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

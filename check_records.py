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
        
        # Look for "記録部屋"
        if await page.is_visible("text=記録部屋"):
            print("Entering 記録部屋...")
            await human_move_and_click(page, "text=記録部屋")
            await asyncio.sleep(5)
            await page.screenshot(path="screenshots/records.png", full_page=True)
            content = await page.content()
            with open("records.html", "w") as f:
                f.write(content)
        else:
            print("記録部屋 not found.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

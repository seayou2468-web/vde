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
        
        await page.screenshot(path="screenshots/main_dashboard.png")
        
        # Check if there are multiple "Internet Courses" or similar
        items = await page.query_selector_all('.item') # Assuming items have class item
        for item in items:
            text = await item.inner_text()
            print(f"Dashboard item: {text.strip()}")

        await page.click("text=東京書籍 インターネット講座")
        await asyncio.sleep(5)
        
        # In course list, check for any other tabs again
        tabs = await page.query_selector_all('.tab')
        for tab in tabs:
            print(f"Course Tab: {await tab.inner_text()}")
            
        # Check all subjects for progress
        subjects = await page.query_selector_all('.dataRow[data-group="on"]')
        for i in range(len(subjects)):
            name = await (await subjects[i].query_selector('.name')).inner_text()
            # Try to see if there is any visible progress percentage
            # Looking at HTML, there's a canvas. Maybe there's a data attribute?
            progress_canvas = await subjects[i].query_selector('canvas.progress')
            # Check for any text in the textBox other than name and startTime
            text_box = await subjects[i].query_selector('.textBox')
            inner = await text_box.inner_text()
            print(f"S{i+1}: {inner.replace('\n', ' | ')}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

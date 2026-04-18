import asyncio
import sys
import os
import random
sys.path.append('/home/jules/self_created_tools')
from human_sim import human_move_and_click, human_type
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        page.on("dialog", lambda dialog: asyncio.create_task(dialog.accept()))

        print("Logging in...")
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await human_type(page, 'input#loginId', "e25040")
        await human_type(page, 'input#passwd', "Puze2968")
        await human_move_and_click(page, 'input#loginBtn')
        await asyncio.sleep(5)
        
        await page.click("text=東京書籍 インターネット講座")
        await asyncio.sleep(5)
        
        # Subject 25
        print("Clicking S25...")
        await human_move_and_click(page, '.dataRow[data-group="on"] >> nth=24')
        await asyncio.sleep(5)
        
        # L6 (might have a different ID, let's find it by index or text)
        lectures = await page.query_selector_all('#contentsPropertyList .rw.data2')
        # Audit said L6 is incomplete. Let's find by name "6"
        target = None
        for l in lectures:
            name_el = await l.query_selector('.lectureName')
            name = await name_el.inner_text() if name_el else ""
            if name.strip() == "6":
                target = l
                break
        
        if target:
            tid = await target.get_attribute('id')
            print(f"Targeting {name} (ID: {tid})")
            
            # Use JS to get coordinates to bypass Playwright's visibility check if needed
            # but still use mouse to click
            box = await page.evaluate("""(id) => {
                const el = document.getElementById(id);
                el.scrollIntoView({block: 'center'});
                const r = el.getBoundingClientRect();
                return {x: r.left, y: r.top, width: r.width, height: r.height, visible: r.width > 0 && r.height > 0};
            }""", tid)
            
            print(f"Box: {box}")
            
            if box['visible']:
                tx = box['x'] + box['width']/2
                ty = box['y'] + box['height']/2
                await page.mouse.move(tx, ty, steps=10)
                await asyncio.sleep(0.5)
                await page.mouse.click(tx, ty)
                print("Clicked.")
                await asyncio.sleep(10)
                
                await page.screenshot(path="screenshots/single_test_after_click.png")
                
                if await page.is_visible('#mPlayer:not(.hidden)'):
                    print("SUCCESS: Player opened!")
                else:
                    print("FAILED: Player still hidden.")
                    # Check if it's pict player
                    if await page.is_visible('#mPictPlayer:not(.hidden)'):
                        print("It's a PictPlayer!")
            else:
                print("Element not visible according to JS.")
        else:
            print("Target lecture not found.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

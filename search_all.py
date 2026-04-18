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
        
        subjects_elements = await page.query_selector_all('.dataRow[data-group="on"]')
        num_subjects = len(subjects_elements)
        
        for i in range(num_subjects):
            subjects_elements = await page.query_selector_all('.dataRow[data-group="on"]')
            subject = subjects_elements[i]
            subject_name = await (await subject.query_selector('.name')).inner_text()
            
            await human_move_and_click(page, f'.dataRow[data-group="on"] >> nth={i}')
            await asyncio.sleep(3)
            
            lectures = await page.query_selector_all('#contentsPropertyList .rw.data2')
            unwatched_count = 0
            for lecture in lectures:
                complete = await lecture.get_attribute('data-complete')
                classes = await lecture.get_attribute('class')
                is_test = 'test' in classes if classes else False
                if complete != 'on' and not is_test:
                    unwatched_count += 1
            
            print(f"Subject: {subject_name} | Unwatched: {unwatched_count}/{len(lectures)}")
            
            await human_move_and_click(page, '#lectureBack')
            await asyncio.sleep(2)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

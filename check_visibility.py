import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await page.fill('input#loginId', "e25040")
        await page.fill('input#passwd', "Puze2968")
        await page.click('input#loginBtn')
        await asyncio.sleep(5)
        
        await page.click("text=東京書籍 インターネット講座")
        await asyncio.sleep(5)
        
        # S25
        await page.click('.dataRow[data-group="on"] >> nth=24')
        await asyncio.sleep(5)
        
        tid = 'lsi63199'
        res = await page.evaluate("""(id) => {
            const el = document.getElementById(id);
            if (!el) return "NOT FOUND";
            const rect = el.getBoundingClientRect();
            const center_x = rect.left + rect.width / 2;
            const center_y = rect.top + rect.height / 2;
            const topEl = document.elementFromPoint(center_x, center_y);
            return {
                id: el.id,
                rect: rect,
                topElId: topEl ? topEl.id : "null",
                topElClass: topEl ? topEl.className : "null",
                topElTag: topEl ? topEl.tagName : "null",
                innerHTML: el.innerHTML
            };
        }""", tid)
        import json
        print(json.dumps(res, indent=2, ensure_ascii=False))
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

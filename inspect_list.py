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
        
        # Subject 9
        await page.click('.dataRow[data-group="on"] >> nth=8')
        await asyncio.sleep(5)
        
        # Get all rows in #contentsPropertyList deeply
        rows = await page.evaluate("""() => {
            const list = document.getElementById('contentsPropertyList');
            if (!list) return "LIST NOT FOUND";
            // The items might be deeper. Let's find all elements with data-complete
            const items = list.querySelectorAll('[data-complete]');
            return Array.from(items).map(el => ({
                id: el.id,
                tag: el.tagName,
                className: el.className,
                complete: el.getAttribute('data-complete'),
                text: el.innerText.substring(0, 30).replace(/\\n/g, ' '),
                visible: el.offsetWidth > 0 && el.offsetHeight > 0
            }));
        }""")
        import json
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

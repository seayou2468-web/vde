import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await page.fill("#loginId", "e25040")
        await page.fill("#passwd", "Puze2968")
        await page.click("#loginBtn")
        await page.wait_for_url("**/mypage**")
        await page.click("#serviceLinkLms")
        await asyncio.sleep(15)

        target = "701 情報Ⅱ"
        await page.evaluate(f"""
            (name) => {{
                const all = document.querySelectorAll('*');
                for (const el of all) {{
                    if (el.innerText.includes(name) && el.innerText.includes('前回視聴') && el.children.length === 0) {{
                        let c = el.parentElement;
                        while(c && !c.innerText.includes(name)) c = c.parentElement;
                        if (c) {{ c.click(); return; }}
                    }}
                }}
            }}
        """, target)
        await asyncio.sleep(10)

        # Take screenshot of lesson list
        await page.screenshot(path="verify_lessons_list.png")

        # Dump lesson statuses
        lessons = await page.evaluate("""
            () => {
                const results = [];
                const items = document.querySelectorAll('#contentsPropertyList .item');
                items.forEach(it => {
                    const text = it.innerText.trim().replace(/\\n/g, ' ');
                    const hasPlay = !!it.querySelector('.play');
                    const watched = !!it.querySelector('.status.on') || it.innerText.includes('視聴済');
                    results.push({ text, hasPlay, watched });
                });
                return results;
            }
        """)
        for l in lessons:
            print(l)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

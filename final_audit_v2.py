import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await page.fill("#loginId", "e25040"); await page.fill("#passwd", "Puze2968")
        await page.click("#loginBtn"); await page.wait_for_url("**/mypage**")
        await page.click("#serviceLinkLms"); await asyncio.sleep(15)

        checked = []
        total_unwatched = 0

        while True:
            target = await page.evaluate(f"""
                (checked) => {{
                    const all = document.querySelectorAll('*');
                    for (const el of all) {{
                        if (el.innerText.includes('前回視聴') && el.children.length === 0) {{
                            let c = el.parentElement;
                            while(c && !c.innerText.includes('701') && !c.innerText.includes('002') && !c.innerText.includes('050')) c = c.parentElement;
                            if (c) {{
                                const name = c.innerText.split('\\n')[0].trim();
                                if (!checked.includes(name)) {{
                                    c.scrollIntoView();
                                    const r = c.getBoundingClientRect();
                                    return {{ name, x: r.x + r.width/2, y: r.y + r.height/2 }};
                                }}
                            }}
                        }}
                    }}
                    return null;
                }}
            """, checked)

            if not target: break
            print(f"Auditing: {target['name']}")
            await page.mouse.click(target['x'], target['y']); await asyncio.sleep(8)

            unwatched = await page.evaluate("""
                () => {
                    const res = [];
                    const items = document.querySelectorAll('#contentsPropertyList .item');
                    items.forEach(it => {
                        if (it.querySelector('.play') && !it.querySelector('.status.on') && !it.innerText.includes('視聴済')) {
                            res.push(it.innerText.trim().replace(/\\n/g, ' '));
                        }
                    });
                    return res;
                }
            """)
            if unwatched:
                print(f"  !!! Found {len(unwatched)} unwatched videos in {target['name']}")
                for u in unwatched: print(f"    - {u}")
                total_unwatched += len(unwatched)
            else:
                print("  All watched.")

            checked.append(target['name'])
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk"); await asyncio.sleep(8)

        print(f"\nFINAL AUDIT COMPLETE. TOTAL UNWATCHED: {total_unwatched}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

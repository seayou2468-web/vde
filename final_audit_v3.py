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

        # Get list of all courses first
        courses = await page.evaluate("""
            () => {
                const res = [];
                const all = document.querySelectorAll('*');
                for (const el of all) {
                    if (el.innerText.includes('前回視聴') && el.children.length === 0) {
                        let c = el.parentElement;
                        while(c && !c.innerText.includes('701') && !c.innerText.includes('002') && !c.innerText.includes('050')) c = c.parentElement;
                        if (c) {
                            const name = c.innerText.split('\\n')[0].trim();
                            if (name !== '講座一覧') res.push(name);
                        }
                    }
                }
                return [...new Set(res)];
            }
        """)

        print(f"Auditing {len(courses)} courses...")
        total_unwatched = 0

        for cname in courses:
            print(f"Checking: {cname}")
            # Click course
            await page.evaluate(f"""
                (name) => {{
                    const all = document.querySelectorAll('*');
                    for (const el of all) {{
                        if (el.innerText.includes('前回視聴') && el.children.length === 0) {{
                            let c = el.parentElement;
                            while(c && !c.innerText.includes(name)) c = c.parentElement;
                            if (c && c.innerText.includes(name)) {{
                                c.scrollIntoView();
                                c.click();
                                return;
                            }}
                        }}
                    }}
                }}
            """, cname)
            await asyncio.sleep(10)

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
                print(f"  !!! Found {len(unwatched)} unwatched in {cname}")
                total_unwatched += len(unwatched)
            else:
                print("  OK.")

            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk"); await asyncio.sleep(8)

        print(f"\nFINAL AUDIT RESULT: {total_unwatched} UNWATCHED VIDEOS REMAINING.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

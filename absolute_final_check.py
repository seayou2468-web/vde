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

        # Get all course items by searching for '前回視聴'
        courses_raw = await page.evaluate("""
            () => {
                const results = [];
                const all = document.querySelectorAll('*');
                for (const el of all) {
                    if (el.innerText.includes('前回視聴') && el.children.length === 0) {
                        let c = el.parentElement;
                        // Walk up to find the container that likely has the name as its first text node
                        while(c && !c.innerText.includes('701') && !c.innerText.includes('002') && !c.innerText.includes('050')) {
                             c = c.parentElement;
                        }
                        if (c) {
                             const name = c.innerText.split('\\n')[0].trim();
                             results.push(name);
                        }
                    }
                }
                return [...new Set(results)].filter(n => n && n !== '前回視聴' && n !== '講座一覧');
            }
        """)

        print(f"Total courses to audit: {len(courses_raw)}")
        grand_total_unwatched = 0

        for cname in courses_raw:
            print(f"Checking {cname}...", end=" ")
            # Find and click
            success = await page.evaluate(f"""
                (name) => {{
                    const all = document.querySelectorAll('*');
                    for (const el of all) {{
                        if (el.innerText.includes(name) && el.innerText.includes('前回視聴') && el.children.length === 0) {{
                            let c = el.parentElement;
                            while(c && !c.innerText.includes(name)) c = c.parentElement;
                            if (c) {{
                                c.scrollIntoView();
                                c.click();
                                return true;
                            }}
                        }}
                    }}
                    return false;
                }}
            """, cname)

            if not success:
                print("FAILED TO CLICK")
                continue

            await asyncio.sleep(8)
            unwatched = await page.evaluate("""
                () => {
                    const items = document.querySelectorAll('#contentsPropertyList .item');
                    let count = 0;
                    items.forEach(it => {
                        if (it.querySelector('.play') && !it.querySelector('.status.on') && !it.innerText.includes('視聴済')) {
                            count++;
                        }
                    });
                    return count;
                }
            """)
            if unwatched > 0:
                print(f"FAILED: {unwatched} unwatched videos")
                grand_total_unwatched += unwatched
            else:
                print("OK")

            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await asyncio.sleep(8)

        print(f"\nGRAND TOTAL UNWATCHED: {grand_total_unwatched}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

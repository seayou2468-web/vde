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

        courses = await page.evaluate("""
            () => {
                const res = [];
                const all = document.querySelectorAll('*');
                for (const el of all) {
                    if (el.innerText.includes('前回視聴') && el.children.length === 0) {
                        let c = el.parentElement;
                        while(c && !c.innerText.includes('701') && !c.innerText.includes('002')) c = c.parentElement;
                        if (c) {
                            const name = c.innerText.split('\\n')[0].trim();
                            const r = c.getBoundingClientRect();
                            if (r.top > 140) res.push({ name, x: r.x + r.width/2, y: r.y + r.height/2 });
                        }
                    }
                }
                return res.filter((v, i, a) => a.findIndex(t => t.name === v.name) === i);
            }
        """)

        print(f"Checking {len(courses)} courses...")
        total_unwatched = 0
        for c in courses:
            print(f"Course: {c['name']}")
            await page.mouse.click(c['x'], c['y'])
            await asyncio.sleep(10)

            lessons = await page.evaluate("""
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
            if lessons:
                print(f"  Unwatched ({len(lessons)}):")
                for l in lessons: print(f"    - {l}")
                total_unwatched += len(lessons)
            else:
                print("  All watched.")

            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await asyncio.sleep(10)

        print(f"\nTOTAL UNWATCHED: {total_unwatched}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

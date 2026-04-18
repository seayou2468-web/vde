import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 5000})
        page = await context.new_page()
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await page.fill("#loginId", "e25040")
        await page.fill("#passwd", "Puze2968")
        await page.click("#loginBtn")
        await page.wait_for_url("**/mypage**")
        await page.click("#serviceLinkLms")
        await asyncio.sleep(15)

        # Get all courses
        courses = await page.evaluate("""
            () => {
                const results = [];
                const rows = document.querySelectorAll('.dataRow');
                rows.forEach(row => {
                    const name = row.innerText.split('\\n')[0].trim();
                    if (name && name !== 'タイトル') {
                        const r = row.getBoundingClientRect();
                        results.push({ name, x: r.x + r.width/2, y: r.y + r.height/2 });
                    }
                });
                return results;
            }
        """)

        print(f"Total courses found: {len(courses)}")
        for c in courses:
            print(f"Course: {c['name']}")
            await page.mouse.click(c['x'], c['y'])
            await asyncio.sleep(8)

            stats = await page.evaluate("""
                () => {
                    const items = document.querySelectorAll('#contentsPropertyList .item');
                    let total = 0, watched = 0, tests = 0;
                    items.forEach(it => {
                        if (it.querySelector('.play')) {
                            total++;
                            if (it.querySelector('.status.on') || it.innerText.includes('視聴済')) {
                                watched++;
                            }
                        }
                        if (it.innerText.includes('テスト') || it.innerText.includes('点')) {
                            tests++;
                        }
                    });
                    return { total, watched, tests };
                }
            """)
            print(f"  Videos: {stats['watched']}/{stats['total']} | Tests: {stats['tests']}")
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await asyncio.sleep(8)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

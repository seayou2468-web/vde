import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 3000}) # Large height to see all
        page = await context.new_page()

        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await page.fill("#loginId", "e25040")
        await page.fill("#passwd", "Puze2968")
        await page.click("#loginBtn")
        await page.wait_for_url("**/mypage**")
        await page.click("#serviceLinkLms")
        await asyncio.sleep(15)

        # Extract courses using the working logic
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
                            if (name && name !== '講座一覧' && name !== '視聴済') {
                                const r = c.getBoundingClientRect();
                                res.push({ name, x: r.x + r.width/2, y: r.y + r.height/2 });
                            }
                        }
                    }
                }
                return res.filter((v, i, a) => a.findIndex(t => t.name === v.name) === i);
            }
        """)

        print(f"Total Courses to verify: {len(courses)}")
        summary = []

        for c in courses:
            print(f"Verifying {c['name']}...")
            await page.mouse.click(c['x'], c['y'])
            await asyncio.sleep(10)

            unwatched_list = await page.evaluate("""
                () => {
                    const items = document.querySelectorAll('#contentsPropertyList .item');
                    const results = [];
                    items.forEach(it => {
                        if (it.querySelector('.play') && !it.querySelector('.status.on') && !it.innerText.includes('視聴済')) {
                            results.push(it.innerText.trim().replace(/\\n/g, ' '));
                        }
                    });
                    return results;
                }
            """)

            if unwatched_list:
                print(f"  FAILED: {len(unwatched_list)} unwatched.")
                summary.append((c['name'], len(unwatched_list)))
            else:
                print("  SUCCESS: All watched.")
                summary.append((c['name'], 0))

            # Go back
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await asyncio.sleep(10)

        print("\n=== FINAL SUMMARY ===")
        total_remaining = 0
        for name, count in summary:
            print(f"{name}: {'OK' if count == 0 else f'{count} REMAINING'}")
            total_remaining += count
        print(f"\nTOTAL REMAINING: {total_remaining}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

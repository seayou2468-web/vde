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

        # Get list of all courses
        courses = await page.evaluate("""
            () => {
                const res = [];
                const all = document.querySelectorAll('.dataRow');
                all.forEach(el => {
                    const name = el.innerText.split('\\n')[0].trim();
                    if (name && name !== 'タイトル') res.push(name);
                });
                return [...new Set(res)];
            }
        """)

        print(f"Total courses to check: {len(courses)}")
        for cname in courses:
            print(f"Checking {cname}...")
            # Click course
            await page.evaluate(f"""
                (name) => {{
                    const els = document.querySelectorAll('.dataRow');
                    for (const el of els) {{
                        if (el.innerText.includes(name)) {{
                            el.scrollIntoView();
                            el.click();
                            return;
                        }}
                    }}
                }}
            """, cname)
            await asyncio.sleep(5)

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
                print(f"  -> {unwatched} unwatched videos!")
            else:
                print("  -> All watched.")

            # Use back button
            await page.click("#kyokaBack")
            await asyncio.sleep(3)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

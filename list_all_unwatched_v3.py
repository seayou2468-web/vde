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

        # Get course list manually
        text = await page.evaluate("() => document.body.innerText")
        lines = text.split('\n')
        courses = []
        for i, line in enumerate(lines):
            if ('701' in line or '002' in line or '050' in line) and len(line) < 100:
                if i+1 < len(lines) and '前回視聴' in lines[i+1]:
                    courses.append(line.strip())

        print(f"Checking {len(courses)} courses: {courses}")

        for cname in courses:
            print(f">>> Course: {cname}")
            await page.evaluate(f"""
                (name) => {{
                    const els = document.querySelectorAll('*');
                    for (const el of els) {{
                        if (el.innerText.includes(name) && el.innerText.includes('前回視聴') && el.children.length === 0) {{
                            let c = el.parentElement;
                            while(c && !c.innerText.includes(name)) c = c.parentElement;
                            if (c) {{ c.click(); return; }}
                        }}
                    }}
                }}
            """, cname)
            await asyncio.sleep(8)

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
                print(f"  UNWATCHED: {len(unwatched)}")
                for u in unwatched[:5]: print(f"    - {u}")
            else:
                print("  ALL WATCHED")

            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await asyncio.sleep(8)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 2000}) # Large viewport to see all
        page = await context.new_page()
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await page.fill("#loginId", "e25040")
        await page.fill("#passwd", "Puze2968")
        await page.click("#loginBtn")
        await page.wait_for_url("**/mypage**")
        await page.click("#serviceLinkLms")
        await asyncio.sleep(15)

        # Extract ALL courses by scrolling if necessary, or just using a large viewport
        courses = await page.evaluate("""
            () => {
                const results = [];
                // The courses are likely in a table or list that might be scrollable
                const allNodes = document.querySelectorAll('*');
                for (const el of allNodes) {
                    if (el.innerText.includes('前回視聴') && el.children.length === 0) {
                        let c = el.parentElement;
                        // Find the row container
                        while(c && !c.classList.contains('dataRow')) c = c.parentElement;
                        if (c) {
                            const name = c.innerText.split('\\n')[0].trim();
                            const r = c.getBoundingClientRect();
                            results.push({ name, y: r.top + r.height/2, x: r.left + r.width/2 });
                        }
                    }
                }
                return results.filter((v, i, a) => a.findIndex(t => t.name === v.name) === i);
            }
        """)

        print(f"Total Courses Identified: {len(courses)}")
        for i, c in enumerate(courses):
            print(f"{i}: {c['name']} (Y={c['y']})")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

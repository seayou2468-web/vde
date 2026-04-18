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

        # Take a screenshot of the main course list
        await page.screenshot(path="final_course_list.png")

        # Click the first course that is not "視聴済" or "講座一覧"
        target = await page.evaluate("""
            () => {
                const all = document.querySelectorAll('*');
                for (const el of all) {
                    if (el.innerText.includes('前回視聴') && el.children.length === 0) {
                        let c = el.parentElement;
                        while(c && !c.innerText.includes('701') && !c.innerText.includes('002')) c = c.parentElement;
                        if (c) {
                            const name = c.innerText.split('\\n')[0].strip();
                            const r = c.getBoundingClientRect();
                            if (r.top > 140) return { name, x: r.x + r.width/2, y: r.y + r.height/2 };
                        }
                    }
                }
                return null;
            }
        """)

        if target:
            print(f"Entering course for final check: {target['name']}")
            await page.mouse.click(target['x'], target['y'])
            await asyncio.sleep(10)
            await page.screenshot(path="final_lesson_list.png")

            lessons = await page.evaluate("""
                () => {
                    const items = document.querySelectorAll('#contentsPropertyList .item');
                    return Array.from(items).map(it => ({
                        text: it.innerText.trim().replace(/\\n/g, ' '),
                        hasPlay: !!it.querySelector('.play'),
                        watched: !!it.querySelector('.status.on') || it.innerText.includes('視聴済')
                    }));
                }
            """)
            print(f"Lessons in {target['name']}:")
            for l in lessons:
                print(f"  [{'X' if l['watched'] else ' '}] {l['text']} (HasPlay: {l['hasPlay']})")
        else:
            print("No courses found for final check.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import random
import time
import sys
from playwright.async_api import async_playwright

watched_courses = set()

async def human_click(page, element, name="element"):
    if not element: return False
    try:
        await element.scroll_into_view_if_needed()
        await asyncio.sleep(0.5)
        box = await element.bounding_box()
        if not box: return False
        x = box['x'] + box['width'] * random.uniform(0.3, 0.7)
        y = box['y'] + box['height'] * random.uniform(0.3, 0.7)
        await page.mouse.move(x, y, steps=random.randint(20, 40))
        await asyncio.sleep(0.3)
        await page.mouse.click(x, y)
        return True
    except: return False

async def watch_video(page):
    print("  Watching video...", flush=True)
    await asyncio.sleep(10)
    # Red play button click
    await page.evaluate("""
        () => {
            const all = document.querySelectorAll('*');
            for (const el of all) {
                if (el.offsetWidth > 0 && el.offsetHeight > 0) {
                    const style = window.getComputedStyle(el);
                    const bg = style.backgroundColor;
                    if (bg.includes('rgb(255, 0, 0)') || bg === 'red') {
                        el.click(); return;
                    }
                }
            }
        }
    """)
    await asyncio.sleep(5)
    # Speed to 2.0x
    await page.evaluate("""
        () => {
            const speedToggle = Array.from(document.querySelectorAll('div, span'))
                .find(el => (el.innerText.includes('標準') || el.innerText.includes('×1.')) && el.offsetWidth > 0);
            if (speedToggle) speedToggle.click();
        }
    """)
    await asyncio.sleep(2)
    await page.evaluate("""
        () => {
            const x2 = Array.from(document.querySelectorAll('div, span'))
                .find(el => el.innerText.includes('×2.0') && el.offsetWidth > 0);
            if (x2) x2.click();
        }
    """)
    await asyncio.sleep(2)

    try:
        total = 0
        for _ in range(15):
            d_text = await page.inner_text("#pictPlayerTool-duration2")
            if d_text and ":" in d_text and d_text != "0:00":
                m, s = map(int, d_text.split(':'))
                total = m * 60 + s
                break
            await asyncio.sleep(2)

        if total > 0:
            target = total * 0.71
            print(f"    Duration: {total}s, Target: {target:.1f}s", flush=True)
            start = time.time()
            while True:
                curr_text = await page.inner_text("#pictPlayerTool-duration1")
                if curr_text and ":" in curr_text:
                    parts = curr_text.split(':')
                    if len(parts) == 2:
                        c_sec = int(parts[0])*60 + int(parts[1])
                        print(f"      Progress: {c_sec}/{total}", flush=True)
                        if c_sec >= target: break

                if await page.is_visible("#testQuestionFrame"): return "test"

                await asyncio.sleep(15)
                if time.time() - start > (total / 2) + 180: break
            return "done"
    except: pass
    return "error"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        print("Logging in...", flush=True)
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await page.fill("#loginId", "e25040")
        await page.fill("#passwd", "Puze2968")
        await page.click("#loginBtn")
        await page.wait_for_url("**/mypage**")
        await page.click("#serviceLinkLms")
        await asyncio.sleep(15)

        while True:
            # Find next course
            target_course = await page.evaluate(f"""
                (watched) => {{
                    const all = document.querySelectorAll('*');
                    for (const el of all) {{
                        if (el.innerText.includes('前回視聴') && el.children.length === 0) {{
                            let container = el.parentElement;
                            while(container && !container.innerText.includes('701') && !container.innerText.includes('002')) container = container.parentElement;
                            if (container) {{
                                const name = container.innerText.split('\\n')[0].trim();
                                if (!watched.includes(name)) {{
                                    const r = container.getBoundingClientRect();
                                    if (r.top > 140 && r.height > 50) return {{ name, x: r.x + r.width/2, y: r.y + r.height/2 }};
                                }}
                            }}
                        }}
                    }}
                    return null;
                }}
            """, list(watched_courses))

            if not target_course: break
            print(f"\n>>> Course: {target_course['name']}", flush=True)
            await page.mouse.click(target_course['x'], target_course['y'])
            await asyncio.sleep(10)

            while True:
                lesson = await page.evaluate("""
                    () => {
                        const items = document.querySelectorAll('#contentsPropertyList .item');
                        for (let i = 0; i < items.length; i++) {
                            const it = items[i];
                            if (it.querySelector('.play') && !it.querySelector('.status.on') && !it.innerText.includes('視聴済')) {
                                const r = it.getBoundingClientRect();
                                return { index: i, text: it.innerText.trim().replace(/\\n/g, ' '), x: r.x + r.width/2, y: r.y + r.height/2 };
                            }
                        }
                        return null;
                    }
                """)
                if not lesson: break

                print(f"  Watching: {lesson['text']}", flush=True)
                await page.mouse.click(lesson['x'], lesson['y'])
                await asyncio.sleep(10)

                res = await watch_video(page)
                if res == "test":
                    btn = await page.query_selector("#test2Back")
                    if btn: await human_click(page, btn)
                else:
                    btn = await page.query_selector("#pictPlayerTool-next")
                    if btn: await human_click(page, btn)
                await asyncio.sleep(10)

            watched_courses.add(target_course['name'])
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await asyncio.sleep(10)

        print("FINISHED ALL", flush=True)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import random
import time
from playwright.async_api import async_playwright

async def human_click(page, element):
    if not element: return False
    try:
        await element.scroll_into_view_if_needed()
        box = await element.bounding_box()
        if not box: return False
        await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2, steps=20)
        await page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
        return True
    except: return False

async def watch_video(page):
    print("  Watching video...", flush=True)
    await asyncio.sleep(10)
    # Red button
    await page.evaluate("""
        () => {
            const all = document.querySelectorAll('*');
            for (const el of all) {
                if (el.offsetWidth > 0 && el.offsetHeight > 0) {
                    const style = window.getComputedStyle(el);
                    if (style.backgroundColor.includes('rgb(255, 0, 0)') || style.backgroundColor === 'red') {
                        el.click(); return;
                    }
                }
            }
        }
    """)
    await asyncio.sleep(5)
    # 2.0x
    await page.evaluate("""
        () => {
            const speedToggle = Array.from(document.querySelectorAll('div, span'))
                .find(el => (el.innerText.includes('標準') || el.innerText.includes('×1.')) && el.offsetWidth > 0);
            if (speedToggle) speedToggle.click();
        }
    """)
    await asyncio.sleep(2); await page.evaluate("""
        () => {
            const x2 = Array.from(document.querySelectorAll('div, span'))
                .find(el => el.innerText.includes('×2.0') && el.offsetWidth > 0);
            if (x2) x2.click();
        }
    """)
    await asyncio.sleep(2)
    try:
        total = 0
        for _ in range(10):
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
                        if c_sec >= target: break
                if await page.is_visible("#testQuestionFrame"): return "test"
                await asyncio.sleep(15)
                if time.time() - start > (total / 2) + 120: break
            return "done"
    except: pass
    return "error"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await page.fill("#loginId", "e25040"); await page.fill("#passwd", "Puze2968")
        await page.click("#loginBtn"); await page.wait_for_url("**/mypage**")
        await page.click("#serviceLinkLms"); await asyncio.sleep(15)

        # Specified courses to skip (already checked or likely checked)
        skipped = ["数Ⅰ002-905 改訂版 新数学Ⅰ", "数A002-905 改訂版 新数学A", "科人002-901 改訂 科学と人間生活", "生基002-902 改訂 新編生物基礎", "書Ⅰ002-901 書道Ⅰ", "CⅠ002-901 All Aboard ! English CommunicationⅠRevised", "論Ⅰ002-901 NEW FAVORITE English Logic and ExpressionⅠRevised", "家総002-901 家庭総合", "情Ⅰ002-901 新編情報Ⅰ", "701 論理・表現Ⅱ NEW FAVORITE English Logic and Expression Ⅱ"]

        while True:
            # Find next course by text and scroll
            target = await page.evaluate(f"""
                (skipped) => {{
                    const all = document.querySelectorAll('*');
                    for (const el of all) {{
                        if (el.innerText.includes('前回視聴') && el.children.length === 0) {{
                            let c = el.parentElement;
                            while(c && !c.innerText.includes('701') && !c.innerText.includes('002')) c = c.parentElement;
                            if (c) {{
                                const name = c.innerText.split('\\n')[0].trim();
                                if (!skipped.includes(name)) {{
                                    c.scrollIntoView();
                                    const r = c.getBoundingClientRect();
                                    return {{ name, x: r.x + r.width/2, y: r.y + r.height/2 }};
                                }}
                            }}
                        }}
                    }}
                    return null;
                }}
            """, skipped)

            if not target: break
            print(f"\n>>> Course: {target['name']}", flush=True)
            await page.mouse.click(target['x'], target['y']); await asyncio.sleep(10)

            while True:
                lesson = await page.evaluate("""
                    () => {
                        const container = document.getElementById('contentsPropertyList');
                        if (!container) return null;
                        const items = container.querySelectorAll('.item');
                        for (let i = 0; i < items.length; i++) {
                            const it = items[i];
                            if (it.querySelector('.play') && !it.querySelector('.status.on') && !it.innerText.includes('視聴済')) {
                                it.scrollIntoView();
                                const r = it.getBoundingClientRect();
                                return { index: i, text: it.innerText.trim().replace(/\\n/g, ' '), x: r.x + r.width/2, y: r.y + r.height/2 };
                            }
                        }
                        return null;
                    }
                """)
                if not lesson: break
                print(f"  Watching: {lesson['text']}", flush=True)
                await page.mouse.click(lesson['x'], lesson['y']); await asyncio.sleep(10)
                res = await watch_video(page)
                if res == "test":
                    btn = await page.query_selector("#test2Back")
                    if btn: await human_click(page, btn)
                else:
                    btn = await page.query_selector("#pictPlayerTool-next")
                    if btn: await human_click(page, btn)
                await asyncio.sleep(10)

            skipped.append(target['name'])
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk"); await asyncio.sleep(10)

        print("COMPLETED", flush=True)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

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

        courses = [
            "701 情報Ⅱ", "701 政治・経済", "701 文学国語", "701 世界史探究", "701 新編論理国語",
            "701 日本史探究", "701 英語コミュニケーションⅡ All Aboard English CommunicationⅡ",
            "701 現代高等保健体育", "現国002-901 新編現代の国語", "言文002-901 新編言語文化",
            "地総002-901 地理総合", "歴総002-901 歴史総合", "公共002-901 公共",
            "数Ⅰ002-905 改訂版 新数学Ⅰ", "数A002-905 改訂版 新数学A", "科人002-901 改訂 科学と人間生活",
            "生基002-902 改訂 新編生物基礎", "書Ⅰ002-901 書道Ⅰ", "CⅠ002-901 All Aboard ! English CommunicationⅠRevised",
            "論Ⅰ002-901 NEW FAVORITE English Logic and ExpressionⅠRevised", "家総002-901 家庭総合",
            "情Ⅰ002-901 新編情報Ⅰ", "050-901現代高等保健体育 改訂版／体育実技", "050-901 音楽Ⅰ 改訂版 Tutti+",
            "701 論理・表現Ⅱ NEW FAVORITE English Logic and Expression Ⅱ"
        ]

        for cname in courses:
            print(f"> {cname}:", end=" ", flush=True)
            clicked = await page.evaluate(f"""
                (name) => {{
                    const els = document.querySelectorAll('*');
                    for (const el of els) {{
                        if (el.innerText.includes(name) && el.innerText.includes('前回視聴') && el.children.length === 0) {{
                            let c = el.parentElement;
                            while(c && !c.innerText.includes(name)) c = c.parentElement;
                            if (c) {{ c.scrollIntoView(); c.click(); return true; }}
                        }}
                    }}
                    return false;
                }}
            """, cname)

            if not clicked:
                print("NOT FOUND")
                continue

            await asyncio.sleep(6)
            unwatched = await page.evaluate("""
                () => document.querySelectorAll('#contentsPropertyList .item .play:not(.on)').length
            """)
            # Since my logic for 'watched' might be slightly off in plain CSS, let's use the one with status.on
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
            if unwatched > 0: print(f"{unwatched} UNWATCHED")
            else: print("OK")

            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await asyncio.sleep(6)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

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
        await page.click("#serviceLinkLms"); await asyncio.sleep(20)

        print(f"Final URL: {page.url}")

        # Capture all text
        text = await page.evaluate("() => document.body.innerText")
        print(f"Total Text Length: {len(text)}")
        if "701" in text: print("Found 701")
        if "情報" in text: print("Found 情報")
        if "前回視聴" in text: print("Found 前回視聴")

        # Check for tables
        tables = await page.evaluate("() => document.querySelectorAll('table').length")
        print(f"Tables: {tables}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

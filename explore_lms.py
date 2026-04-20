import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("Logging in...")
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login?")
        await page.fill("#loginId", "e25040")
        await page.fill("#passwd", "Puze2968")
        await page.click("#loginBtn")

        await page.wait_for_selector("#serviceLinkLms")
        await page.click("#serviceLinkLms")

        print("Waiting for LMS app to load...")
        # Wait for the main container or some expected element
        await page.wait_for_selector("#mSubject", state="visible")

        # Take a screenshot of the subjects
        await page.screenshot(path="subjects.png", full_page=True)

        # Explore the subjects
        subjects = await page.query_selector_all("#subjectList .item")
        print(f"Found {len(subjects)} subjects")

        for i, subject in enumerate(subjects):
            title_el = await subject.query_selector(".title")
            title = await title_el.inner_text() if title_el else "No title"
            print(f"Subject {i}: {title}")

            # Check for completion status if visible
            status_el = await subject.query_selector(".status")
            status = await status_el.inner_text() if status_el else ""
            print(f"  Status: {status}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

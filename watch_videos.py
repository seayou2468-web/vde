import asyncio
import random
import sys
import os

# Add self_created_tools to path
sys.path.append('/home/jules/self_created_tools')

from human_sim import HumanSim
from visual_utils import human_visual_click
from playwright.async_api import async_playwright

async def set_speed_2x(sim):
    print("UI: Setting speed 2.0x...")
    try:
        # Toggle menu
        if not await sim.page.is_visible('#menuList:not(.closeMenu)'):
            if await sim.click_element('#menuCtrl'):
                await asyncio.sleep(8)
        
        speed_opt = await sim.page.get_by_text("再生速度").first.element_handle()
        if speed_opt:
            await sim.click_element(speed_opt)
            await asyncio.sleep(8)
            opt_2x = await sim.page.get_by_text("×2.0").first.element_handle()
            if opt_2x:
                await sim.click_element(opt_2x)
                await asyncio.sleep(4)
                print("UI: Speed set to 2.0x")
        
        if await sim.page.is_visible('#menuList:not(.closeMenu)'):
            await sim.click_element('#menuCtrl')
            await asyncio.sleep(3)
    except Exception as e:
        print(f"Speed set failed: {e}")

async def ensure_playing(sim, ptype):
    try:
        if ptype == "video":
            is_paused = await sim.page.evaluate("document.getElementById('playerVideo').paused")
            if is_paused:
                print("Action: Play video...")
                await sim.click_element('#playerVideo')
        else:
            status = await sim.page.get_attribute('#pictPlayerTool-play', 'data-value')
            if status == 'off':
                print("Action: Play slides...")
                await sim.click_element('#pictPlayerTool-play')
    except Exception as e:
        print(f"Ensure playing failed: {e}")

async def is_player_open(page):
    url = page.url
    if '#pp-' in url: return True
    v_vis = await page.is_visible('#mPlayer:not(.hidden)')
    p_vis = await page.is_visible('#mPictPlayer:not(.hidden)')
    return v_vis or p_vis

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-setuid-sandbox'
        ])
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = await context.new_page()
        sim = HumanSim(page)
        
        page.on("dialog", lambda d: asyncio.create_task(d.accept()))

        print("--- LOGIN ---")
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/login")
        await sim.type_text('#loginId', "e25040")
        await sim.type_text('#passwd', "Puze2968")
        await sim.click_element('#loginBtn')
        await asyncio.sleep(20)
        
        print("--- DASHBOARD ---")
        await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
        await asyncio.sleep(30)

        targets = [
            '言文002-901 新編言語文化', '歴総002-901 歴史総合', '公共002-901 公共',
            '数Ⅰ002-905 改訂版 新数学Ⅰ', '数A002-905 改訂版 新数学A', '科人002-901 改訂 科学と人間生活', 
            '生基002-902 改訂 新編生物基礎', '書Ⅰ002-901 書道Ⅰ', 'CⅠ002-901 All Aboard ! English CommunicationⅠRevised', 
            '論Ⅰ002-901 NEW FAVORITE English Logic and ExpressionⅠRevised', '家総002-901 家庭総合', 
            '情Ⅰ002-901 新編情報Ⅰ', '050-901現代高等保健体育 改訂版／体育実技', '050-901 音楽Ⅰ 改訂版 Tutti+', 
            '701 論理・表現Ⅱ NEW FAVORITE English Logic and Expression Ⅱ', '地総002-901 地理総合', 
            '現国002-901 新編現代の国語', '701 政治・経済', '701 文学国語', '701 世界史探究', '701 新編論理国語', 
            '701 英語コミュニケーションⅡ All Aboard English CommunicationⅡ'
        ]

        while True:
            # Periodic browser restart could be added here if needed
            subjects = await page.query_selector_all('.dataRow')
            if not subjects:
                print("No subjects found. Reloading dashboard...")
                await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
                await asyncio.sleep(30)
                subjects = await page.query_selector_all('.dataRow')
                if not subjects: break

            target_sub = None
            target_name = ""
            
            random.shuffle(targets)
            for tname in targets:
                for s in subjects:
                    if tname[:10] in await s.inner_text():
                        comp_el = await s.query_selector('.comp')
                        if comp_el:
                            comp_text = await comp_el.inner_text()
                            if '/' in comp_text:
                                done, tot = [x.strip() for x in comp_text.split('/')]
                                if done == tot and tot != "0": continue
                        target_sub = s; target_name = tname; break
                if target_sub: break
            
            if not target_sub:
                print("All targets complete or none found.")
                break
            
            print(f"--- ENTERING SUBJECT: {target_name} ---")
            await sim.click_element(target_sub)
            await asyncio.sleep(30)
            
            if not await page.is_visible('#contentsPropertyList'):
                print("Lecture list failed. Returning to dashboard.")
                await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
                await asyncio.sleep(20)
                continue

            # Expansion
            for cls in ['.rw.data1.close', '.expandable.contract']:
                units = await page.query_selector_all(cls)
                for u in units:
                    await sim.click_element(u)
                    await asyncio.sleep(5)

            while True:
                lectures = await page.query_selector_all('.rw.data2')
                target_lec = None
                for l in lectures:
                    is_comp = await l.get_attribute('data-complete') == 'on'
                    classes = await l.get_attribute('class') or ''
                    if not is_comp and 'test' not in classes:
                        if await l.is_visible():
                            target_lec = l; break
                
                if not target_lec:
                    print(f"Subject {target_name} session finished.")
                    break
                
                lid = await target_lec.get_attribute('id')
                print(f"Targeting Lecture: {lid}")
                await sim.hover_element(target_lec)
                await asyncio.sleep(5)
                
                opened = False
                box = await target_lec.bounding_box()
                if box:
                    points = [0.72, 0.75, 0.85, 0.68, 0.5]
                    for p in points:
                        tx = box['x'] + box['width'] * p
                        ty = box['y'] + box['height'] / 2
                        print(f"Clicking row at {p*100}% width...")
                        await sim.click_at(tx, ty)
                        # Wait for player or URL change
                        for _ in range(15): # 45s total
                            await asyncio.sleep(3)
                            if await is_player_open(page): 
                                opened = True; break
                        if opened: break
                        if not await page.is_visible('#contentsPropertyList'):
                             await asyncio.sleep(10)
                             if await is_player_open(page): opened = True; break

                if not opened:
                    if await human_visual_click(sim, target_lec):
                        for _ in range(15):
                            await asyncio.sleep(3)
                            if await is_player_open(page): opened = True; break

                if not opened:
                    print(f"FAIL to open {lid}. Breaking.")
                    await page.screenshot(path=f"screenshots/fail_{lid}.png")
                    break 

                ptype = "video" if await page.is_visible('#mPlayer:not(.hidden)') else "pict"
                print(f"Status: Watching {ptype}...")
                
                await set_speed_2x(sim)
                await ensure_playing(sim, ptype)
                
                last_pos = -1; stuck = 0; start_t = asyncio.get_event_loop().time()
                while True:
                    try:
                        await page.bring_to_front()
                        if ptype == "video":
                            ended = await page.evaluate("document.getElementById('playerVideo').ended")
                            pos = await page.evaluate("document.getElementById('playerVideo').currentTime")
                        else:
                            cur = await page.inner_text('#pictPlayerTool-duration1')
                            tot = await page.inner_text('#pictPlayerTool-duration2')
                            ended = (cur == tot and tot != "0:00")
                            pos = cur
                        if ended: break
                        if pos == last_pos:
                            stuck += 1
                            if stuck > 20: # 3+ mins stuck
                                print("Stuck? Re-triggering play.")
                                await ensure_playing(sim, ptype); stuck = 0
                        else: stuck = 0
                        last_pos = pos
                        if asyncio.get_event_loop().time() - start_t > 3600: break
                        await asyncio.sleep(10) # Faster poll for log activity
                    except: break
                
                print("Content finished. Returning to list.")
                back_sel = None
                for b in ['#player1Back', '#pictPlayerTool-back', '#lectureBack']:
                    if await page.is_visible(b): back_sel = b; break
                
                if back_sel:
                    await sim.click_element(back_sel)
                    await asyncio.sleep(30)
                else:
                    await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
                    await asyncio.sleep(30)
                    break 

            print("Refreshing dashboard...")
            await page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await asyncio.sleep(25)

        await browser.close()

if __name__ == "__main__":
    import os
    from visual_utils import find_red_clusters
    os.makedirs("screenshots", exist_ok=True)
    asyncio.run(run())

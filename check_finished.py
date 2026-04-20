import asyncio
import sys
import os
from self_created_tools.playback_engine import PlaybackEngine

async def main():
    engine = PlaybackEngine("e25040", "Puze2968")
    try:
        await engine.start()
        await engine.login()
        count = await engine.get_course_count()
        total_unfinished = 0
        for i in range(count):
            await engine.enter_course(i)
            rows = await engine.page.query_selector_all(".rw.data2")
            unfinished_in_course = 0
            for row in rows:
                is_test = await row.query_selector(".play.test")
                complete = await row.get_attribute("data-complete")
                if not is_test and complete == "off":
                    play_icon = await row.query_selector(".item.play.movie")
                    if play_icon:
                        unfinished_in_course += 1
            print(f"Course {i}: {unfinished_in_course} unfinished videos.")
            total_unfinished += unfinished_in_course

            # Go back
            await engine.page.goto("https://kouza.tokyo-shoseki.co.jp/oslms/app#kk")
            await engine.page.wait_for_selector(".dataCell.kyoka", timeout=30000)

        print(f"Total unfinished videos: {total_unfinished}")
    finally:
        await engine.stop()

if __name__ == "__main__":
    asyncio.run(main())

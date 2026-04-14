import asyncio
from self_created_tools.playback_engine import PlaybackEngine

async def main():
    engine = PlaybackEngine("e25040", "Puze2968")
    try:
        await engine.start()
        await engine.login()
        count = await engine.get_course_count()
        print(f"Found {count} courses.")
        if count > 0:
            await engine.enter_course(8) # 新編現代の国語
            print("Successfully entered course 8.")
            await engine.back_to_courses()
            print("Successfully returned to courses.")
    finally:
        await engine.stop()

if __name__ == "__main__":
    asyncio.run(main())

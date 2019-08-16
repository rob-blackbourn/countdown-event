"""Example For CountdownEvent"""

import asyncio
from countdown_event import CountdownEvent

async def main_async():

    countdown_event = CountdownEvent()

    async def mock_job(sleep_time: float) -> None:
        nonlocal countdown_event
        count = countdown_event.increment()
        print(f'incremented count to {count}')
        try:
            await asyncio.sleep(sleep_time)
        finally:
            count = countdown_event.decrement()
            print(f'decremented count to {count}')

    async def wait_on_countdown_event():
        nonlocal countdown_event
        print('waiting for zero event')
        await countdown_event.wait()
        print('zero event cleared')
        
    tasks = [asyncio.create_task(mock_job(5)) for _ in range(5)]
    tasks.append(wait_on_countdown_event())

    await asyncio.wait(tasks)
    assert countdown_event.count == 0
    print("done")

if __name__ == "__main__":
    asyncio.run(main_async())

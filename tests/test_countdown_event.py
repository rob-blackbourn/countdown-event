"""Test For CountdownEvent"""

import asyncio
import pytest
from countdown_event import CountdownEvent

@pytest.mark.asyncio
async def test_smoke():
    """Smoke test"""
    await asyncio.sleep(1)
    assert True

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

    tasks = [asyncio.create_task(mock_job(5)) for _ in range(5)]
    tasks.append(countdown_event.wait())

    await asyncio.wait(tasks)
    assert countdown_event.count == 0
    print("done")

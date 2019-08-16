"""Cancellation on a countdown event"""

import asyncio
from countdown_event import CountdownEvent

async def long_running_task(
        countdown_event: CountdownEvent,
        cancellation_event: asyncio.Event
) -> None:
    count = countdown_event.increment()
    print(f'incremented count to {count}')
    try:
        print('Waiting for cancellation event')
        await cancellation_event.wait()
    finally:
        count = countdown_event.decrement()
        print(f'decremented count to {count}')

async def set_cancellation_event(
        seconds_to_wait: float,
        countdown_event: CountdownEvent,
        cancellation_event: asyncio.Event
) -> None:
    print(f'waiting {seconds_to_wait} seconds before setting the cancellation event')
    await asyncio.sleep(seconds_to_wait)
    print('setting the cancellation event')
    cancellation_event.set()
    print('waiting for tasks to finish')
    await countdown_event.wait()
    print('countdown event cleared')

async def main_async():

    cancellation_event = asyncio.Event()
    countdown_event = CountdownEvent()

    tasks = [
        long_running_task(countdown_event, cancellation_event),
        long_running_task(countdown_event, cancellation_event),
        long_running_task(countdown_event, cancellation_event),
        set_cancellation_event(5, countdown_event, cancellation_event)
    ]

    await asyncio.wait(tasks)
    assert countdown_event.count == 0
    print("done")

if __name__ == "__main__":
    asyncio.run(main_async())

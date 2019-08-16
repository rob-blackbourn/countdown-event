# countdown-event

A synchronization class which blocks when the count is not zero.

Here's an example

```python
import asyncio
from countdown_event import CountdownEvent

async def long_running_task(countdown_event,cancellation_event):
    count = countdown_event.increment()
    print(f'incremented count to {count}')
    try:
        print('Waiting for cancellation event')
        await cancellation_event.wait()
    finally:
        count = countdown_event.decrement()
        print(f'decremented count to {count}')

async def stop_tasks(secs, countdown_event, cancellation_event):
    print(f'waiting {secs} seconds before setting the cancellation event')
    await asyncio.sleep(secs)
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
        stop_tasks(5, countdown_event, cancellation_event)
    ]
    await asyncio.wait(tasks)
    assert countdown_event.count == 0
    print("done")

if __name__ == "__main__":
    asyncio.run(main_async())
```

Here's the output.

```
incremented count to 1
Waiting for cancellation event
incremented count to 2
Waiting for cancellation event
waiting 5 seconds before setting the cancellation event
incremented count to 3
Waiting for cancellation event
setting the cancellation event
waiting for tasks to finish
decremented count to 2
decremented count to 1
decremented count to 0
countdown event cleared
done
```
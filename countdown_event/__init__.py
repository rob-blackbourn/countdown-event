"""Countdown Event"""


from asyncio import Event


class CountdownEvent:
    """An event which blocks when not zero"""

    def __init__(self)-> None:
        self._event = Event()
        self._count = 0
        self._event.set()

    def increment(self) -> int:
        """Increment the count
        
        :return: The current count
        :rtype: int
        """
        self._count += 1
        self._event.clear()
        return self._count

    def decrement(self) -> int:
        """Decrement the count
        
        :return: The current count
        :rtype: int
        """
        assert self._count > 0, "Count cannot go below zero"
        self._count -= 1
        if self._count == 0:
            self._event.set()
        return self._count

    async def wait(self) -> None:
        """Wait for the count to be zero"""
        await self._event.wait()

    @property
    def count(self) -> int:
        """The current count
        
        :return: The current count
        :rtype: int
        """
        return self._count

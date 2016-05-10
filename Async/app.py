from collections import namedtuple
import asyncio

Task = namedtuple('Task', ['func', 'interval', 'repeat'])


class Main(object):

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.clock_ticks = 0
        self.tasks = []

    async def clock(self):
        for task in (task for task in self.tasks if self.clock_ticks % task.interval is 0):
            asyncio.ensure_future(task.func())
            if not task.repeat:
                self.tasks.remove(task)
        await asyncio.sleep(1)
        self.clock_ticks += 1
        asyncio.Task(self.clock())

    def add_task(self, func, interval, repeat=False):
        self.tasks.append(Task(func, interval, repeat))

    def dtime(self, ticks):
        return self.clock_ticks + ticks

    def start(self):
        asyncio.Task(self.clock())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.stop()
        finally:
            self.loop.close()
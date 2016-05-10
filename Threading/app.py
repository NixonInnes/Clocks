import time
from collections import namedtuple
from threading import Thread

Task = namedtuple('Task', ['func', 'interval', 'repeat'])


class Clock(Thread):
    def __init__(self, func):
        self.func = func
        super().__init__(self, name='Clock')
        self.setDaemon(True)

    def run(self):
        while True:
            time.sleep(1)
            self.func()


class Main(object):

    def __init__(self):
        self.clock_ticks = 0
        self.tasks = []
        self.clock = Clock()

    def do_tasks(self):
        for task in (task for task in self.tasks if self.clock_ticks % task.interval is 0):
            task.func()
            if not task.repeat:
                self.tasks.remove(task)
        self.clock_ticks += 1

    def add_task(self, func, interval, repeat=False):
        self.tasks.append(Task(func, interval, repeat))

    def dtime(self, ticks):
        return self.clock_ticks + ticks
import asyncio
import threading

from CommentsRecorder import CommentsRecorder
from taskscreator import taskcreator

import logging
import logging.config

logging.config.fileConfig("logger.conf")

lock = threading.Lock()
commentq = []
numq = []

recorder = CommentsRecorder(lock, commentq, numq)
upers = taskcreator(lock, commentq, numq)

recorder.start()
asyncio.ensure_future(upers.creating())

loop = asyncio.get_event_loop()
loop.set_debug(True)
try:
    loop.run_forever()
except:
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.run_forever()

loop.close()

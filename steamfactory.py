import logging
import signal
from collections import namedtuple
from multiprocessing import JoinableQueue, Process, cpu_count

logger = logging.getLogger(__name__)

Task = namedtuple('Task', 'function,args,kwargs')


class Factory:
    """Like a Pool, but workers must work, not swim!
    """

    def __init__(self, size=None, autostart=True, max_queue_size=None):
        self.size = size or cpu_count()
        if max_queue_size is None:
            max_queue_size = self.size * 3
        self.max_queue_size = max_queue_size
        if autostart:
            self.start()

    def worker_process(self, idx, queue):
        # SIGINT is handled by controller process
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        logger.info('[Worker {}] Starting up'.format(idx))
        while True:
            if queue.empty():
                logger.info('[Worker {}] Idling...'.format(idx))
            job = queue.get(block=True)
            logger.info('[Worker {}] Accepted new task: {}'.format(idx, job))
            logger.info('Queue size is now {}'.format(queue.qsize()))

            try:
                job.function(*job.args, **job.kwargs)
            except:
                logger.exception(
                    '[Worker {}] Exception raised while running task'
                    .format(idx))
            finally:
                queue.task_done()

    def start(self):
        if getattr(self, '_running', False):
            return
        self._running = True

        logger.info('Starting factory...')
        self.queue = JoinableQueue(self.max_queue_size)
        self.workers = []
        for x in range(self.size):
            proc = Process(target=self.worker_process, args=(x, self.queue,),
                           daemon=True)
            self.workers.append(proc)
            proc.start()

    def run(self, func, *args, **kwargs):
        self.queue.put(Task(func, args, kwargs))

    def shutdown(self):
        logger.info('Shutting down (waiting for tasks to complete)')
        self.queue.close()
        self.queue.join()
        logger.info('-' * 80)
        logger.info('Processing complete. Shutting down workers')
        self.terminate()

    def terminate(self):
        for idx, proc in enumerate(self.workers):
            logger.info('Shutting down worker {} (pid {})'
                        .format(idx, proc.pid))
            proc.terminate()
            proc.join()
        self._running = False

import logging
import os
import random
import sys
import time

from steamfactory import Factory

if sys.version_info < (3,):
    raise RuntimeError('Unsupported Python version. Required Python 3')


colors = [
    148, 139, 50, 93, 160, 95, 141, 166, 214, 79, 186, 185, 162, 28,
    32, 39, 145, 142, 158, 36, 187, 151, 138, 231, 181, 105, 159, 199,
    42, 94, 128, 113, 85, 207, 34, 84, 230, 202, 196, 193, 155, 45,
    35, 47, 195, 86, 179, 192, 136, 33, 203, 75, 117, 49, 164, 198,
    205, 112, 43, 153, 208, 59, 72, 134, 188, 37, 26, 41, 201, 101,
    172, 167, 216, 132, 76, 204, 83, 97, 87, 163, 206, 209, 40, 81,
    150, 44, 92, 129, 98, 103, 194, 69, 109, 213, 63, 223, 176, 78,
    31, 102, 106, 62, 169, 226, 51, 173, 140, 135, 118, 30, 170, 73,
    157, 174, 96, 70, 116, 168, 108, 46, 224, 127, 184, 80, 100, 111,
    71, 74, 107, 189, 165, 115, 38, 220, 60, 210, 66, 146, 120, 171,
    110, 152, 130, 228, 161, 191, 104, 61, 212, 219, 137, 217, 222,
    123, 114, 227, 218, 68, 99, 133, 131, 125, 180, 121, 229, 221,
    143, 197, 183, 200, 67, 156, 82, 154, 144, 147, 215, 177, 48, 122,
    27, 190, 65, 225, 175, 119, 211, 64, 178, 77, 126, 182, 149, 29]


logger = logging.getLogger(__name__)


class MyHandler(logging.StreamHandler):

    def format(self, record):
        pid = os.getpid()
        color = colors[pid % len(colors)]

        prefix = '\x1b[38;5;{}m{}\x1b[0m'.format(color, pid)
        formatted = super().format(record)
        return '{} {}'.format(prefix, formatted)


handler = MyHandler(sys.stderr)
handler.setFormatter(logging.Formatter(
    '\x1b[1m%(levelname)s\x1b[0m \x1b[33m%(name)s\x1b[0m: %(message)s'
))
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)


def do_something(x):
    logger.info('Doing something: {}'.format(x))
    time.sleep(random.random() * 5)
    logger.info('DONE: {}'.format(x))


def do_fail(x):
    logger.info('Raising an exception in 3.. 2.. 1..')
    raise ValueError('Hey, this is an exception!')


if __name__ == '__main__':
    factory = Factory()

    try:
        for x in range(1000):
            logger.info('Scheduling task {}'.format(x))

            func = do_something
            if x > 10 and random.random() <= .1:
                func = do_fail

            factory.run(func, x)
            time.sleep(.1)

    except KeyboardInterrupt:
        logger.info('Shutting down...')

    factory.shutdown()

import time
from steamfactory import Factory


def do_nothing():
    time.sleep(1)


# Create a factory, running up to 4 tasks concurrently
factory = Factory(size=4)

for _ in range(4):
    factory.run(do_nothing)

# Wait for tasks to be consumed, then quit. Prevents the main
# process from exiting while tasks are still running
factory.shutdown()

Steam factory
#############

Replacement for multiprocessing's Pool, offering more powerful
features. Allow running a generic Python function asynchronously.


Example usage
=============

First, we are going to need a function that does something. In this
case, it does nothing more than waiting one second.

.. code-block:: python

    import time

    def do_nothing():
        time.sleep(1)
        print('Sleeping done')  # If you want some feedback..


To run this function in parallel, we're going to need a ``Factory`` instance.

.. code-block:: python

    from steamfactory import Factory

    # Create a factory, running up to 4 tasks concurrently
    factory = Factory(size=4)

All set, we can schedule some async function executions:

.. code-block:: python

    for _ in range(4):
        factory.run(do_nothing)

After a second, you should see the four "Sleeping done" messages being
printed at once.

In case you're using this inside a script, and you need the main
process to wait for all tasks to be executed before terminating
(meaning that tasks will be lost), remember to call the ``shutdown()``
method:

.. code-block:: python

    factory.shutdown()


Getting feedback
================

How to get "feedback" from the tasks usually greatly depends on the
application. Many times you don't even bother with the function return
value, you just need something to be done. Other times values might be
large, or the required retention time might vary.

The library doesn't currently offer any way to return results to the
caller, but you can easily do something like this:

.. code-block:: python

    import time
    from multiprocessing import Manager

    from steamfactory import Factory

    _mgr = Manager()
    results = _mgr.dict()  # Shared between processes


    def addup(a, b):
        time.sleep(1)
        results[(a, b)] = a + b

    # Create a factory, running up to 4 tasks concurrently
    factory = Factory(size=4)

    # Let's schedule some tasks
    factory.run(addup, 1, 2)
    factory.run(addup, 3, 4)
    factory.run(addup, 5, 6)
    factory.run(addup, 7, 8)

    factory.shutdown()

    # Now, results contains all the results (after a 1s processing
    # time)

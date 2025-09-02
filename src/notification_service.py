import asyncio
import threading
from desktop_notifier import DesktopNotifier

# 1. Create a new asyncio event loop.

_loop = asyncio.new_event_loop()


def _start_background_loop(loop):
    """Function to run the event loop in the background thread."""
    asyncio.set_event_loop(loop)
    loop.run_forever()


# 2. Create and start a daemon thread to run the loop.
#    A daemon thread will exit automatically when the main app closes.

_thread = threading.Thread(target=_start_background_loop, args=(_loop,), daemon=True)
_thread.start()

# 3. Create a single, reusable notifier instance.

_notifier = DesktopNotifier()


def show_notification(title, message):
    """
    Shows a notification by safely scheduling the async 'send' method
    on the dedicated background event loop.
    """
    coro = _notifier.send(title=title, message=message)

    # 4. Use run_coroutine_threadsafe to schedule the task from our
    #    main Qt thread onto the background asyncio thread.

    asyncio.run_coroutine_threadsafe(coro, _loop)

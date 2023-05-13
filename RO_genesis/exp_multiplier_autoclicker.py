from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Listener

import threading
import time

keyboard = Controller()
stop_event = threading.Event()


def press_space():
    while not stop_event.is_set():
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        time.sleep(5.5)


def on_click(x, y, button, pressed):
    if button == Button.right:
        stop_event.set()
        return False


# Start the spacebar pressing thread
space_thread = threading.Thread(target=press_space)
space_thread.start()

# Listen for right-click on the mouse
with Listener(on_click=on_click) as listener:
    listener.join()

# Wait for the spacebar thread to finish
space_thread.join()

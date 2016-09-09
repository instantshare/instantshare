import logging
import threading

from tools.toolbox import Platform

_name = "hotkeys"


class HotkeyInUseError(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg


class Hotkey(Platform):
    def __init__(self, event_queue):
        self.event_queue = event_queue

        self.add_hotkey = lambda: None
        self.remove_hotkey = lambda: None
        self.listen = lambda: None

        super().__init__()

    def init_osx(self):
        pass

    def init_linux(self):
        pass

    def init_windows(self):
        from pyhooked import KeyboardEvent, Hook

        _defined_hotkeys = {}

        def add_hotkey(list_of_keys, callback):
            # Use an immutable set as dictionary key (eliminates duplicate keys)
            list_as_frozenset = frozenset(list_of_keys)

            # Raise exception when hotkey is already in use
            if list_as_frozenset in _defined_hotkeys:
                raise HotkeyInUseError("Hotkey '{0}' is already in use.".format("+".join(list_as_frozenset)))

            _defined_hotkeys[list_as_frozenset] = callback

        def remove_hotkey(list_of_keys):
            # Use an immutable set as dictionary key (eliminates duplicate keys)
            frozen_set_of_keys = frozenset(list_of_keys)
            _defined_hotkeys.pop(frozen_set_of_keys, None)

        def handle_events(args):
            if isinstance(args, KeyboardEvent):
                # Check if a defined hotkey was pressed and trigger its callback
                for hotkey in _defined_hotkeys.keys():
                    if set(hotkey).issubset(args.pressed_key) and args.event_type == "key down":
                        logging.debug("Defined hotkey '{0}' was pressed.".format("+".join(hotkey)))

                        hotkey_callback = _defined_hotkeys[hotkey]
                        self.event_queue.put(hotkey_callback)

        def listen():
            hk = Hook()  # make a new instance of PyHooked
            hk.handler = handle_events  # add callback for occuring events
            logging.debug("Starting hotkey listener daemon..")
            thread = threading.Thread(target=hk.hook, daemon=True)
            thread.start()  # start listening on new thread

        self.add_hotkey = add_hotkey
        self.remove_hotkey = remove_hotkey
        self.listen = listen

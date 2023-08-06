import signal


def setup_sigterm(exit_event):
    # exit_event can be either a single multiprocessing.Event() or a list.
    def terminate(signum, frame):
        if isinstance(exit_event, list):
            for e in exit_event:
                e.set()
        else:
            exit_event.set()

    signal.signal(signal.SIGINT, terminate)
    signal.signal(signal.SIGTERM, terminate)

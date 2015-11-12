from time import sleep


def delay_execution(t, fn):
    sleep(t)
    return fn()

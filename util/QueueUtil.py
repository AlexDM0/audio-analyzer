import queue
import numpy as np

audioQueue = queue.Queue()

def clear_queue(q):
    while not q.empty():
        q.get()


def get_all_items_from_queue(q):
    items = []
    while not q.empty():
        items.append(q.get())
    return np.concatenate(items)


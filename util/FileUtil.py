import soundfile as sf
import time
from util.QueueUtil import get_all_items_from_queue


def store_audio(q, sample_rate):
    res = get_all_items_from_queue(q)
    # get filename based on the current date/time in the format 2024-12-31_23-59-59.wav
    filename = "snapshots/"+time.strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
    sf.write(filename, res, int(sample_rate), 'PCM_24')


def save_volume_data(volume_data):
    filename = "data/data_"+time.strftime("%Y-%m-%d") + ".csv"
    with open(filename, "a") as f:
        for timestamp, volume in volume_data:
            f.write(f"{timestamp},{volume}\n")
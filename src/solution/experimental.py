import pickle
import numpy as np


class FrameCollector:
    def __init__(self):
        self.first_coll = []
        self.sec_col = []
        self.third_coll = []

    def collect_frame(self, frame: np.ndarray, frame_idx: int):
        """
        Capture specified frames and save them into pickle files.
        """
        if 312 >= frame_idx >= 277:
            self.first_coll.append(frame.tolist())
        if 703 >= frame_idx >= 664:
            self.sec_col.append(frame.tolist())
        if 1240 >= frame_idx >= 1210:
            self.third_coll.append(frame.tolist())

    def save(self):
        for arr, name in [
            [self.first_coll, "first.pkl"],
            [self.sec_col, "sec.pkl"],
            [self.third_coll, "third.pkl"],
        ]:
            with open(name, "wb") as file:
                pickle.dump(arr, file)


def read_frame_pickle_and_vis(filename: str):
    """Get a numpy array by reading a pickle file."""
    with open(filename, "rb") as file:
        data = pickle.load(file)
        data = [arr for arr in map(np.array, data)]
    return data


if __name__ == "__main__":
    read_frame_pickle_and_vis("first.pkl")

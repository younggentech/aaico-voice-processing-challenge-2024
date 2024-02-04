import librosa
import numpy as np
import time
import threading
import queue
import pickle

from src.solution.experimental import FrameCollector

########### PARAMETERS ###########
# DO NOT MODIFY
# Desired sample rate 16000 Hz
sample_rate = 16000
# Frame length
frame_length = 512



########### AUDIO FILE ###########
# DO NOT MODIFY
# Path to the audio file
audio_file = "assets/audio_aaico_challenge.wav"

# Read the audio file and resample it to the desired sample rate
audio_data, current_sample_rate = librosa.load(
    audio_file,
    sr=sample_rate,
)
audio_data_int16 = (audio_data * 32767).astype(np.int16)
number_of_frames = len(audio_data_int16) // frame_length
audio_data_int16 = audio_data_int16[:number_of_frames * frame_length]
audio_duration = len(audio_data_int16) / sample_rate


########### STREAMING SIMULATION ###########
# DO NOT MODIFY
results = np.zeros(shape=(3, len(audio_data_int16)), dtype=np.int64)
# Detection mask lines are SENT TIME, LABEL, RECEIVE TIME.
buffer = queue.Queue()
start_event = threading.Event()

def label_samples(list_samples_id, labels):
    receive_time = time.time_ns()
    results[1][list_samples_id] = labels
    results[2][list_samples_id] = receive_time

def notice_send_samples(list_samples_id):
    send_time = time.time_ns()
    results[0][list_samples_id] = send_time

def emit_data():
    time.sleep(.5)
    print('Start emitting')
    start_event.set()
    for i in range(0, number_of_frames):
        list_samples_id = np.arange(i*frame_length, (i+1)*frame_length)
        time.sleep(frame_length / sample_rate) # Simulate real time
        frame = audio_data_int16[list_samples_id]
        buffer.put(frame)
        notice_send_samples(list_samples_id)
    print('Stop emitting')


def process_data():
    i = 0
    start_event.wait()
    print('Start processing')
    f_collector = FrameCollector()  # TODO: DELETE BEFORE PROD
    while i != number_of_frames:
        frame = buffer.get()
        ### TODO: YOUR CODE
        # MODIFY
        # The array was randomly picked from the pool, to check if RMSE can catch it
        fake_frame = np.array([-1006, -643, -210, -104, -330, -313, -476, -537, -620, -588, -453, -203, 79, 345, 420, 328, 544, 791, 468, 173, 614, 647, 416, 180, -4, -294, 129, 363, 290, -90, -181, 1, 296, 363, 470, 801, 475, 107, -2, -127, -552, -201, 270, 47, -383, -386, -249, 97, 180, -113, -489, -443, -35, 357, 233, 43, 15, -209, -477, -373, -59, -382, -759, -626, -525, -830, -618, -37, 413, 558, 628, 354, 63, 154, 81, -364, -233, 355, 612, 452, 176, 273, 236, 0, -138, -368, -792, -882, -559, -410, -545, -199, 299, 169, -195, -236, -147, -49, 120, 10, -124, -105, 8, -120, -493, -700, -546, -430, -381, 67, 365, 497, 487, 659, 769, 636, 551, 481, 339, 57, -140, -201, -125, -39, 26, -44, -191, -17, 134, 151, 529, 879, 864, 641, 453, 167, 181, 347, 333, -18, -504, -725, -718, -609, -410, -317, -356, -98, 233, 285, 83, 120, 232, 107, 143, 386, 243, -23, 74, 285, 132, -228, -494, -725, -775, -493, -191, 38, 253, 306, 148, 58, 264, 732, 731, 416, 198, 11, -102, 3, 126, -109, -208, -281, -91, 197, 295, 46, -46, 146, 250, 185, 176, 115, -152, -266, -294, -128, -51, -265, -327, -404, -654, -396, 53, 94, -4, 151, 478, 789, 894, 634, 371, 281, 298, 406, 472, 178, -174, -170, -154, 8, 131, -44, -386, -420, -515, -422, -99, 267, 418, 373, 405, 481, 297, -105, -191, -264, -308, -460, -421, -708, -687, -290, 107, 266, 297, 142, 325, 600, 454, 299, 201, 152, 94, -73, -671, -916, -847, -778, -718, -249, -261, -206, 68, 268, 343, 633, 821, 698, 419, 17, -108, -369, -554, -518, -237, -611, -890, -628, -254, -31, 474, 550, 115, 34, 310, 445, 370, 407, 270, 86, -244, -542, -631, -555, -630, -518, -419, -364, -84, 203, 251, 383, 484, 330, 283, 145, -321, -459, -130, -170, -323, -212, -141, -141, -116, -93, -60, 13, 42, 233, 538, 474, 275, 144, -26, -110, 40, 237, 406, 212, -215, -275, -28, 70, 34, 44, 199, 214, 337, 687, 756, 675, 739, 733, 365, 71, -61, -116, -355, -691, -941, -972, -808, -600, -378, -179, -60, -104, -31, 196, 392, 364, 190, 98, 82, 112, 226, 287, 46, -269, -302, -111, -121, -388, -449, -281, -95, 249, 566, 576, 378, 280, 580, 713, 434, 180, 134, -32, -275, -276, -211, -300, -398, -319, -252, -248, -168, 77, 342, 121, -275, -153, 116, 115, 6, -82, -341, -507, -447, -216, -199, -469, -531, -261, -31, -104, -151, -175, -205, 62, 451, 239, -248, -401, -215, 67, 271, 144, -131, -344, -334, -194, -360, -509, -424, -456, -569, -359, -84, 5, 38, 215, 219, 93, 269, 325, 10, -135, -199, -243, -5, 222, 208, 92, 172, 450, 426, 150, 144, 151, -29, -28, 334, 507, 114, -111, 122, 329, 456, 630, 634, 601, 609, 520, 494, 424, 309, 179, 208, 370, 413, 109, -89, 145, 338, 339, 518, 612, 61, -403, -271, -111, -340, -535, -684, -761, -560, -316, -22, 263, 304, 352, 549, 522, 395, 314, 146, 160, 369, 425])
        # Subtracted 5 from fake_frame to modify it a bit in case it will become like another frame in the pool
        rmse = np.sqrt(np.mean((frame - (fake_frame-5))**2))
        f_collector.collect_frame(frame, i)
        if rmse < 6:
            print(i, rmse)
        list_samples_id = np.arange(i*frame_length, (i+1)*frame_length)
        labels = [1 for _ in range(len(list_samples_id))]
        ###

        label_samples(list_samples_id, labels)
        i += 1
    print('Stop processing')
    # Save the list to a file
    f_collector.save()  # TODO: DELETE BEFORE PROD
    with open('results.pkl', 'wb') as file:
        pickle.dump(results, file)


if __name__ == "__main__":
    time_measurement = []

    thread_process = threading.Thread(target=process_data)
    thread_emit = threading.Thread(target=emit_data)

    thread_process.start()
    thread_emit.start()
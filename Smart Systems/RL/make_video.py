import cv2
import os


SIZE = 10
POLICY = "greedy"


def make_video():
    # windows:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # Linux:
    #fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    out = cv2.VideoWriter(f'{SIZE}x{SIZE}.mp4',
                          fourcc, 20.0, (1200, 900))

    for i in range(0, 200):
        img_path = f"images/q_learning/{SIZE}x{SIZE}/E_{i}.png"
        print(img_path)
        frame = cv2.imread(img_path)
        out.write(frame)

    out.release()


make_video()

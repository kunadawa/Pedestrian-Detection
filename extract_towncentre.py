import os
import cv2
import numpy as np
import logging as log

#Dataset from http://www.robots.ox.ac.uk/ActiveVision/Research/Projects/2009bbenfold_headpose/project.html#datasets

def video2im(src='TownCentreXVID.avi', train_path='images', test_path='test_images', factor=2):
    """
    Extracts all frames from a video and saves them as jpgs
    """

    try:
        os.mkdir(train_path)
        os.mkdir(test_path)
    except FileExistsError as fee:
        log.error(f"Error creating output directories - {fee.strerror}: {fee.filename}")
        logging.getLogger().setLevel(logging.INFO)
        log.info("delete or rename offending directory")
        return

    frame = 0
    cap = cv2.VideoCapture(src)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print('Total Frame Count:', length )

    while True:
        check, img = cap.read()
        if check:
            if frame < 3600:
                path = train_path
            else:
                path = test_path

            img = cv2.resize(img, (1920 // factor, 1080 // factor))
            cv2.imwrite(os.path.join(path, str(frame) + ".jpg"), img)

            frame += 1
            print('Processed: ',frame, end = '\r')

        else:
            break

    cap.release()

def validate_video_path(path):
    """
    returns a tuple. first element of the tuple indicates whether the validation succeeded
    second element is an optional logging message
    """
    if os.path.exists(path):
        return (True, f"Processing {path}...")
    else:
        return (False, f"{path} does not exist")

# validator=validate_video_path, processor=video2i
def process_video_cmd_args(argv, validator=validate_video_path, processor=video2im):
    """
    calls video2im() with validated path or none (default path to be used) when there are no args passed
    """
    try:
        path = argv[1]
        status, msg = validator(path)
        if status:
            processor(src=path)
            log.info(msg)
        else:
            log.error(msg)
    except IndexError:
        log.warning('Video file path was not passed to script arguements, trying default location, name')
        processor()


if __name__ == '__main__':
    import sys
    process_video_cmd_args(sys.argv, validate_video_path, video2im)

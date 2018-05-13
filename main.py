#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
#

__author__ = '@r0ark'
__version__ = '0.0.1'

import os, sys, time
import cv2, argparse

class VideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)

    def read(self):
        _, frame = self.stream.read()
        return frame

class StopMotionCamera:
    def __init__(self, src=0, fps=6, output=None):
        self.stream = VideoStream(src)

        self.fps = float(fps)
        self.output = output

        self.frames = []

    def save_frames(self, output, fps, frames):
        if output is None:
            output = '-'.join(time.ctime().split(' ')[-2:][::-1]).replace(':', '-') + '.mp4'

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output, fourcc, fps, frames[0].shape[:2][::-1])

        for frame in frames:
            writer.write(frame)

        writer.release()
        return output

    def main(self):
        while True:
            frame = self.stream.read()
            copy_frame = frame.copy()

            cv2.putText(copy_frame, 'Press "Space" to take a frame', (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255] * 3)
            cv2.putText(copy_frame, 'Press "S/s" to save frames to file', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255] * 3)

            cv2.imshow('Stop Motion', copy_frame)
            pressed = cv2.waitKey(5) & 0xFF

            if pressed == 32:
                self.frames.append(frame)
                print('{0} frames, {1} seconds'.format(len(self.frames), len(self.frames) / self.fps))

            elif pressed in list(map(ord, ('S', 's'))):
                filepath = os.path.join(os.getcwd(), self.save_frames(self.output, self.fps, self.frames))
                print('Saved as ' + filepath)

                self.frames = []

            elif pressed in list(map(ord, ('Q', 'q'))) + [27]:
                sys.exit()

if __name__ == '__main__':
    app = StopMotionCamera()
    app.main()
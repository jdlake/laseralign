from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, TLCamera, Frame
from thorlabs_tsi_sdk.tl_camera_enums import SENSOR_TYPE
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK
import typing
import threading
import queue
import cv2
import time
import os
import sys

absolute_path_to_file_directory = os.path.dirname(os.path.abspath(__file__))
relative_path_to_dlls = "\\dll\\64_lib\\"
absolute_path_to_dlls = os.path.abspath(absolute_path_to_file_directory + os.sep + relative_path_to_dlls)
os.environ['PATH'] = absolute_path_to_dlls + os.pathsep + os.environ['PATH']
os.add_dll_directory(absolute_path_to_dlls)



class VideoFrameCapture():
    def __init__(self):
        camSDK = self.getcamSDK()
        cam = self.getcam(camSDK)

        frame = self.getframe(cam)
        image_data = frame.image_buffer
        print(image_data)
        image = cv2.imwrite('jamie1.png', image_data)
        FlippedImage = cv2.flip(image,1)

        self.discon(cam, camSDK)

    @classmethod
    def getcamSDK(cls):
        try:
            camSDK = TLCameraSDK()
            print("SDK Connected")
            return camSDK
        except:
            print("ERROR: Couldn't open SDK")

    @classmethod
    def getcam(cls, camSDK):
        try:
            serial = camSDK.discover_available_cameras()
            cam = camSDK.open_camera(serial[0])
            print("Camera Connected")
            return cam
        except:
            print("Camera couldn't be connected")





    def getframe(self, cam):
        cam.operation_mode = 0
        cam.frames_per_trigger_zero_for_unlimited = 0
        cam.image_poll_timeout_ms = 150
        cam.arm(2)
        cam.issue_software_trigger()
        frame = cam.get_pending_frame_or_null()
        cam.exposure_time_us = 11000
        cam.disarm()
        return frame

    @classmethod
    def discon(cls, cam, sdk):
        try:
            cam.dispose()
            sdk.dispose()
            print("Camera and SDK closed")
        except:
            print("Failed closing camera or SDK")




if __name__ == '__main__':
    frame = VideoFrameCapture()

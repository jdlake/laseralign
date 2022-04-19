from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, TLCamera, Frame
from thorlabs_tsi_sdk.tl_camera_enums import SENSOR_TYPE
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK
from PIL import Image
import typing
import threading
import queue
import time
import os
import sys

absolute_path_to_file_directory = os.path.dirname(os.path.abspath(__file__))
relative_path_to_dlls = "\\dll\\64_lib\\"
absolute_path_to_dlls = os.path.abspath(absolute_path_to_file_directory + os.sep + relative_path_to_dlls)
os.environ['PATH'] = absolute_path_to_dlls + os.pathsep + os.environ['PATH']
os.add_dll_directory(absolute_path_to_dlls)


class Model:
    def __init__(self):
        cam, camSDK = self.getcam()
        frame = self.getframe(cam)
        image_data = frame.image_buffer
        print(image_data)
        pilimage = Image.fromarray(image_data)
        pilimage.save("jamie.png")
        self.disconnect(cam, camSDK)




    def getcam(self):
        camSDK = TLCameraSDK()
        serial = camSDK.discover_available_cameras()
        return camSDK.open_camera(serial[0]), camSDK

    def getframe(self, cam):
        cam.image_poll_timeout_ms = 10000  # 2 second timeout
        cam.arm(1)

        cam.issue_software_trigger()
        time.sleep(0.5)
        frame = cam.get_pending_frame_or_null()
        cam.exposure_time_us = 6000000


        cam.disarm()
        return frame

    def disconnect(self, cam, sdk):
        cam.dispose()
        sdk.dispose()


if __name__ == '__main__':
    camera = Model()

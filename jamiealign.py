from PIL import Image, ImageTk
import typing, threading, os, queue
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, TLCamera, Frame
import numpy as np
import cv2 as cv
import tkinter as tk
import time
#from pympler.tracker import SummaryTracker
#from pympler import classtracker


#tracker = SummaryTracker()

absolute_path_to_file_directory = os.path.dirname(os.path.abspath(__file__))
relative_path_to_dlls = "\\dll\\64_lib\\"
absolute_path_to_dlls = os.path.abspath(absolute_path_to_file_directory + os.sep + relative_path_to_dlls)
os.environ['PATH'] = absolute_path_to_dlls + os.pathsep + os.environ['PATH']
os.add_dll_directory(absolute_path_to_dlls)


class LiveViewCanvas(tk.Canvas):

    def __init__(self, parent, image_queue):
        # type: (typing.Any, queue.Queue) -> LiveViewCanvas
        self.image_queue = image_queue
        self._image_height, self._image_width = 0, 0
        x_, y_ = 0, 0 
        self._temp_height, self._temp_width = 1080, 1920
        tk.Canvas.__init__(self, parent)
        self.create_line(self._temp_width/2,0,self._temp_width/2,self._temp_height, fill="green", width=1)
        self.create_line(0, (self._temp_height)/2, self._temp_width, (self._temp_height)/2, fill="green", width=1)
        self.create_oval(self._temp_width/2-5,self._temp_height/2-5,self._temp_width/2+5,self._temp_height/2+5, outline="green", width=1)
        self.create_oval(self._temp_width / 2 - 30, self._temp_height / 2 - 30, self._temp_width / 2 + 30,
                         self._temp_height / 2 + 30, outline="green", width=1)
        self.create_oval(self._temp_width / 2 - 100, self._temp_height / 2 - 100, self._temp_width / 2 + 100,
                         self._temp_height / 2 + 100, outline="green", width=1)
        self.create_oval(self._temp_width / 2 - 180, self._temp_height / 2 - 180, self._temp_width / 2 + 180,
                         self._temp_height / 2 + 180, outline="green", width=1)
        self.alignmark = self.create_oval(x_,y_,x_,y_, outline='red', width=1)
        self.pack()
        self._get_image()


    def moment_raw(self, r, i, j):
        _x = np.arange(r.shape[0]) ** j
        _y = np.arange(r.shape[1]) ** i
        _XX, _YY = np.meshgrid(_y, _x)
        return (_XX * _YY * r).sum()

    def centroid(self, imagearray):
        _, bin_img = cv.threshold(imagearray, 25, 225, 0)
        moments = cv.moments(bin_img)
        #moments = cv.moments(imagearray)
        if moments['m00'] == 0:
            x_, y_ = 0, 0 
        else:
            x_, y_ = (int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00']))
        return x_, y_


    def _get_image(self):
        try:
            image = self.image_queue.get_nowait()
            image = image.resize((1920  ,   1080))
            imagearray = np.array(image)
            x_, y_ = self.centroid(imagearray)
            self._image = ImageTk.PhotoImage(master=self, image=image)
            if (self._image.width() != self._image_width) or (self._image.height() != self._image_height):
                # resize the canvas to match the new image size
                self._image_width = self._image.width()
                self._image_height = self._image.height()
                self.config(width=self._image_width, height=self._image_height)
            self.tkimage = self.create_image(0, 0, image=self._image, anchor='nw')
            self.lower(self.tkimage)
            self.coords(self.alignmark, x_-2.5,y_-2.5,x_+2.5,y_+2.5)
        except queue.Empty:
            pass
        self.after(16, self._get_image)



class ImageAcquisitionThread(threading.Thread):

    def __init__(self, camera):
        # type: (TLCamera) -> ImageAcquisitionThread
        super(ImageAcquisitionThread, self).__init__()
        self._camera = camera
        self._previous_timestamp = 0
        self._is_color = False
        self._bit_depth = camera.bit_depth
        self._camera.image_poll_timeout_ms = 0
        self._image_queue = queue.Queue(maxsize=2)
        self._stop_event = threading.Event()

    def get_output_queue(self):
        # type: (type(None)) -> queue.Queue
        return self._image_queue

    def stop(self):
        self._stop_event.set()

    def _get_image(self, frame):
        scaled_image = frame.image_buffer >> (self._bit_depth - 8)
        return Image.fromarray(scaled_image)

    def run(self):
        while not self._stop_event.is_set():
            try:
                frame = self._camera.get_pending_frame_or_null()
                if frame is not None:
                    pil_image = self._get_image(frame)
                    self._image_queue.put_nowait(pil_image)
            except queue.Full:
                pass
            except Exception as error:
                print("Encountered error: {error}, image acquisition will stop.".format(error=error))
                break


if __name__ == "__main__":
    with TLCameraSDK() as sdk:
        camera_list = sdk.discover_available_cameras()
        with sdk.open_camera(camera_list[0]) as camera:
            root = tk.Tk()
            root.title("Jamie's alignment app")
            image_acquisition_thread = ImageAcquisitionThread(camera)
            camera_widget = LiveViewCanvas(parent=root, image_queue=image_acquisition_thread.get_output_queue())
            camera.frames_per_trigger_zero_for_unlimited = 0
            camera.arm(2)
            camera.issue_software_trigger()
            camera.exposure_time_us = int(4500)
            time.sleep(0.3)
            image_acquisition_thread.start()

            root.mainloop()
            
            image_acquisition_thread.stop()
            image_acquisition_thread.join()


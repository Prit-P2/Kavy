from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
smile_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]

                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
                if len(eyes) > 0:
                    cv2.putText(frame, "Eyes Detected", (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

                smiles = smile_cascade.detectMultiScale(roi_gray, 1.7, 20)
                if len(smiles) > 0:
                    cv2.putText(frame, "Smiling", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()

if __name__ == '__main__':
    CamApp().run()
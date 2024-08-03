import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import threading

class NetworkCameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Camera Viewer")

        # Create a video frame
        self.video_frame = ttk.Label(root)
        self.video_frame.grid(row=0, column=0, columnspan=2)

        # Create a settings frame
        self.settings_frame = ttk.LabelFrame(root, text="Settings")
        self.settings_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Add settings options
        self.url_label = ttk.Label(self.settings_frame, text="Camera URL:")
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ttk.Entry(self.settings_frame, width=30)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.url_entry.insert(0, "http://your_camera_url_here")

        self.start_button = ttk.Button(self.settings_frame, text="Start", command=self.start_stream)
        self.start_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.stop_button = ttk.Button(self.settings_frame, text="Stop", command=self.stop_stream)
        self.stop_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.running = False
        self.capture_thread = None

    def start_stream(self):
        if not self.running:
            self.running = True
            self.capture_thread = threading.Thread(target=self.capture_video)
            self.capture_thread.start()

    def stop_stream(self):
        if self.running:
            self.running = False
            if self.capture_thread is not None:
                self.capture_thread.join()

    def capture_video(self):
        url = self.url_entry.get()
        cap = cv2.VideoCapture(url)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_frame.imgtk = imgtk
            self.video_frame.configure(image=imgtk)
            self.video_frame.update()

        cap.release()

    def on_closing(self):
        self.stop_stream()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkCameraApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

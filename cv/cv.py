import cv2
import tkinter as tk
from ultralytics import YOLO

# Fetch screen resolution dynamically
_root = tk.Tk()
screen_w = _root.winfo_screenwidth()
screen_h = _root.winfo_screenheight()
_root.destroy()

model = YOLO("yolo26m-seg.pt")

results = model.predict(source="0", show=False, conf=0.60, stream=True)

cv2.namedWindow("YOLO", cv2.WINDOW_NORMAL)

for r in results:
    frame = r.plot()

    h, w = frame.shape[:2]
    scale = min(screen_w / w, screen_h / h)
    cv2.resizeWindow("YOLO", int(w * scale), int(h * scale))

    cv2.imshow("YOLO", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
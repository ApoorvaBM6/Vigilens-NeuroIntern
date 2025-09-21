import cv2

# Open camera (0 = default webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
else:
    print("=== Webcam Info ===")
    print("Frame width:", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("Frame height:", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("FPS (frames per second):", cap.get(cv2.CAP_PROP_FPS))
    print("FourCC codec:", int(cap.get(cv2.CAP_PROP_FOURCC)))
    print("Brightness:", cap.get(cv2.CAP_PROP_BRIGHTNESS))
    print("Contrast:", cap.get(cv2.CAP_PROP_CONTRAST))
    print("Saturation:", cap.get(cv2.CAP_PROP_SATURATION))
    print("Exposure:", cap.get(cv2.CAP_PROP_EXPOSURE))

cap.release()
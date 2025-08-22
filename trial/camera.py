import cv2

def open_camera():
    # Open default camera (0 = first camera, 1 = external webcam, etc.)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Cannot open camera")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If frame not read correctly, break
        if not ret:
            print("❌ Failed to grab frame")
            break

        # Show the frame in a window
        cv2.imshow("Camera Demo", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close window
    cap.release()
    cv2.destroyAllWindows()



open_camera()
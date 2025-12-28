import cv2
from pyzbar.pyzbar import decode

PHONE_CAMERA_URL = "http://10.167.21.119:8080/video"  # dummy IP


def scan_barcode_live():
    cap = cv2.VideoCapture(PHONE_CAMERA_URL)

    if not cap.isOpened():
        raise RuntimeError("❌ Cannot open phone camera stream")

    window_name = "📦 Barcode Scanner (ZBar)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 900, 600)

    print("📷 ZBar scanner started. Scan barcode (Q to quit)")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        barcodes = decode(gray)

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type

            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            text = f"{barcode_data} ({barcode_type})"
            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            print("✅ Barcode detected:", barcode_data)

            cap.release()
            cv2.destroyAllWindows()
            return barcode_data

        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

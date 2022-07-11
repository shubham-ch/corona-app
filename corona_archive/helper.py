from email.mime import image
import cv2
from random import randint

def decode_qr_code(filename: str) -> str:
    """
    Decodes a QR code image fie and returns the data
    """
    img = cv2.imread(filename)
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(img)
    if vertices_array is not None:
        return data
    return None

def random_id() -> int:
    """
    Generates a random integer id
    """
    range_start = 999999999
    range_end = 2147483647
    return randint(range_start, range_end)

def allowedFile(filename: str) -> bool:
    """
    Checks if a given file is a valid image file
    """
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

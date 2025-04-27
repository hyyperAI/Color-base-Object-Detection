# src/utils.py

import os
import cv2
import numpy as np
from PIL import Image
import io
import base64

def create_sample_images():
    os.makedirs('assets', exist_ok=True)
    sample_image_paths = ["assets/color_objects1.jpg", "assets/color_objects2.jpg"]

    if not os.path.exists(sample_image_paths[0]):
        img1 = np.zeros((400, 600, 3), dtype=np.uint8)
        cv2.circle(img1, (150, 150), 70, (0, 0, 255), -1)
        cv2.circle(img1, (400, 150), 60, (0, 255, 0), -1)
        cv2.rectangle(img1, (100, 250), (200, 350), (255, 0, 0), -1)
        cv2.imwrite(sample_image_paths[0], img1)

    if not os.path.exists(sample_image_paths[1]):
        img2 = np.zeros((400, 600, 3), dtype=np.uint8)
        cv2.circle(img2, (100, 100), 50, (0, 255, 255), -1)
        cv2.circle(img2, (300, 150), 80, (0, 0, 255), -1)
        cv2.circle(img2, (500, 100), 60, (255, 0, 0), -1)
        cv2.rectangle(img2, (200, 250), (300, 350), (0, 255, 0), -1)
        cv2.rectangle(img2, (400, 250), (500, 350), (255, 0, 255), -1)
        cv2.imwrite(sample_image_paths[1], img2)

    return sample_image_paths

def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/jpg;base64,{img_str}" download="{filename}">{text}</a>'
    return href

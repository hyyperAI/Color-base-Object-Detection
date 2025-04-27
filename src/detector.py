# src/detector.py

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

from src.config import COLOR_PRESETS, DEFAULT_ERODE_SIZE, DEFAULT_DILATE_SIZE, DEFAULT_MIN_AREA, DEFAULT_CIRCULARITY_THRESHOLD
from src.utils import create_sample_images

class MultiColorDetector:
    def __init__(self):
        self.color_presets = COLOR_PRESETS
        self.erode_size = DEFAULT_ERODE_SIZE
        self.dilate_size = DEFAULT_DILATE_SIZE
        self.min_area = DEFAULT_MIN_AREA
        self.circularity_threshold = DEFAULT_CIRCULARITY_THRESHOLD
        self.sample_images = create_sample_images()

    
    def process_image(self, image, h_low, s_low, v_low, h_high, s_high, v_high,
                      h_low2, h_high2, erode_size, dilate_size, min_area,
                      circularity_threshold, color_name, color_bgr):
        """Process the image to detect objects of the specified color."""
        if image is None:
            return None, None, None, None, None

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_color = np.array([h_low, s_low, v_low])
        upper_color = np.array([h_high, s_high, v_high])
        mask = cv2.inRange(hsv, lower_color, upper_color)

        if h_low2 > 0 and h_high2 > 0:
            lower_color2 = np.array([h_low2, s_low, v_low])
            upper_color2 = np.array([h_high2, s_high, v_high])
            mask2 = cv2.inRange(hsv, lower_color2, upper_color2)
            mask = cv2.bitwise_or(mask, mask2)

        if erode_size > 0:
            erode_kernel = np.ones((erode_size, erode_size), np.uint8)
            mask = cv2.erode(mask, erode_kernel, iterations=1)

        if dilate_size > 0:
            dilate_kernel = np.ones((dilate_size, dilate_size), np.uint8)
            mask = cv2.dilate(mask, dilate_kernel, iterations=1)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = image.copy()
        circular_count = 0
        other_count = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                perimeter = cv2.arcLength(contour, True)
                circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0

                if circularity > circularity_threshold:
                    circular_count += 1
                    cv2.circle(result, center, radius, color_bgr, 2)
                    cv2.putText(result, f"{color_name} Ball ({int(area)})", (center[0] - 40, center[1] - radius - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_bgr, 2)
                else:
                    other_count += 1
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(result, (x, y), (x + w, y + h), color_bgr, 2)
                    cv2.putText(result, f"{color_name} Object ({int(area)})", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_bgr, 2)

        hsv_plot = None
        if len(contours) > 0:
            full_mask = np.zeros_like(mask)
            cv2.drawContours(full_mask, contours, -1, 255, -1)
            h_values = hsv[:, :, 0][full_mask > 0]
            s_values = hsv[:, :, 1][full_mask > 0]

            if len(h_values) > 0:
                fig, ax = plt.subplots(figsize=(4, 4))
                ax.scatter(h_values, s_values, alpha=0.5, s=1)
                ax.set_xlim([0, 180])
                ax.set_ylim([0, 255])
                ax.set_xlabel('Hue')
                ax.set_ylabel('Saturation')
                ax.set_title(f'H-S Distribution of {color_name} Objects')
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                hsv_plot = Image.open(buf)
                plt.close(fig)

        return result, mask, circular_count, other_count, hsv_plot

    def detect_all_colors(self, image, colors_to_detect, params):
        """Detect multiple colors in an image and combine results."""
        if image is None:
            return None, None, {}

        combined_result = image.copy()
        all_masks = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
        detection_stats = {}

        for color in colors_to_detect:
            color_preset = self.color_presets[color]
            h_low = params.get("h_low", color_preset["h_low"]) if color == "Custom" else color_preset["h_low"]
            s_low = params.get("s_low", color_preset["s_low"]) if color == "Custom" else color_preset["s_low"]
            v_low = params.get("v_low", color_preset["v_low"]) if color == "Custom" else color_preset["v_low"]
            h_high = params.get("h_high", color_preset["h_high"]) if color == "Custom" else color_preset["h_high"]
            s_high = params.get("s_high", color_preset["s_high"]) if color == "Custom" else color_preset["s_high"]
            v_high = params.get("v_high", color_preset["v_high"]) if color == "Custom" else color_preset["v_high"]
            h_low2 = params.get("h_low2", color_preset["h_low2"]) if color == "Custom" else color_preset["h_low2"]
            h_high2 = params.get("h_high2", color_preset["h_high2"]) if color == "Custom" else color_preset["h_high2"]

            result, mask, circular_count, other_count, _ = self.process_image(
                image, h_low, s_low, v_low, h_high, s_high, v_high,
                h_low2, h_high2, params["erode_size"], params["dilate_size"],
                params["min_area"], params["circularity_threshold"],
                color_preset["color_name"], color_preset["color_bgr"]
            )

            if result is not None:
                combined_result = cv2.addWeighted(combined_result, 0.7, result, 0.3, 0)

                if mask is not None:
                    all_masks = cv2.bitwise_or(all_masks, mask)

                detection_stats[color] = {
                    "circular": circular_count,
                    "other": other_count,
                    "total": circular_count + other_count
                }

        return combined_result, all_masks, detection_stats

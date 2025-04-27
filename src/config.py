# src/config.py

COLOR_PRESETS = {
    "Red": {"h_low": 0, "s_low": 100, "v_low": 100, "h_high": 10, "s_high": 255, "v_high": 255,
            "h_low2": 170, "h_high2": 180, "color_bgr": (0, 0, 255), "color_name": "Red"},
    "Green": {"h_low": 35, "s_low": 100, "v_low": 100, "h_high": 85, "s_high": 255, "v_high": 255,
              "h_low2": 0, "h_high2": 0, "color_bgr": (0, 255, 0), "color_name": "Green"},
    "Blue": {"h_low": 100, "s_low": 100, "v_low": 100, "h_high": 130, "s_high": 255, "v_high": 255,
             "h_low2": 0, "h_high2": 0, "color_bgr": (255, 0, 0), "color_name": "Blue"},
    "Yellow": {"h_low": 20, "s_low": 100, "v_low": 100, "h_high": 30, "s_high": 255, "v_high": 255,
               "h_low2": 0, "h_high2": 0, "color_bgr": (0, 255, 255), "color_name": "Yellow"},
    "Purple": {"h_low": 130, "s_low": 100, "v_low": 100, "h_high": 160, "s_high": 255, "v_high": 255,
               "h_low2": 0, "h_high2": 0, "color_bgr": (255, 0, 255), "color_name": "Purple"},
    "Orange": {"h_low": 10, "s_low": 100, "v_low": 100, "h_high": 20, "s_high": 255, "v_high": 255,
               "h_low2": 0, "h_high2": 0, "color_bgr": (0, 165, 255), "color_name": "Orange"},
    "Custom": {"h_low": 0, "s_low": 100, "v_low": 100, "h_high": 10, "s_high": 255, "v_high": 255,
               "h_low2": 0, "h_high2": 0, "color_bgr": (255, 255, 255), "color_name": "Custom"}
}

DEFAULT_ERODE_SIZE = 5
DEFAULT_DILATE_SIZE = 5
DEFAULT_MIN_AREA = 500
DEFAULT_CIRCULARITY_THRESHOLD = 0.7

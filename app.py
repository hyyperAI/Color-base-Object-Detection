# app.py

import streamlit as st
import cv2
import numpy as np

from src.detector import MultiColorDetector
from src.utils import get_image_download_link
from PIL import Image

def main():
    st.set_page_config(layout="wide", page_title="Multi-Color Object Detector")

    st.title("Multi-Color Object Detection")
    st.markdown("""
        This application demonstrates classical computer vision techniques for color-based object detection
        using HSV thresholding, morphological operations, and shape analysis.
    """)

    detector = MultiColorDetector()

    st.sidebar.header("Input Settings")
    input_option = st.sidebar.radio(
        "Choose input source",
        ["Sample Image 1", "Sample Image 2", "Upload Image"]
    )

    detection_mode = st.sidebar.radio(
        "Detection Mode",
        ["Single Color", "Multiple Colors"]
    )

    st.sidebar.header("Detection Settings")
    erode_size = st.sidebar.slider("Erode Size", 0, 20, detector.erode_size)
    dilate_size = st.sidebar.slider("Dilate Size", 0, 20, detector.dilate_size)
    min_area = st.sidebar.slider("Minimum Area", 100, 3000, detector.min_area)
    circularity_threshold = st.sidebar.slider("Circularity Threshold", 0.1, 1.0, detector.circularity_threshold)

    params = {
        "erode_size": erode_size,
        "dilate_size": dilate_size,
        "min_area": min_area,
        "circularity_threshold": circularity_threshold
    }

    image = None
    if input_option == "Sample Image 1":
        image = cv2.imread(detector.sample_images[0])
    elif input_option == "Sample Image 2":
        image = cv2.imread(detector.sample_images[1])
    elif input_option == "Upload Image":
        uploaded_file = st.sidebar.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is not None:
        if detection_mode == "Single Color":
            selected_color = st.sidebar.selectbox(
                "Select Color",
                list(detector.color_presets.keys())
            )
            params.update(detector.color_presets[selected_color])
            result, mask, ball_count, other_count, hsv_plot = detector.process_image(
                image,
                params["h_low"], params["s_low"], params["v_low"],
                params["h_high"], params["s_high"], params["v_high"],
                params.get("h_low2", 0), params.get("h_high2", 0),
                params["erode_size"], params["dilate_size"],
                params["min_area"], params["circularity_threshold"],
                params["color_name"], params["color_bgr"]
            )

            col1, col2 = st.columns(2)

            with col1:
                st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Original Image", use_column_width=True)
                st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), caption="Detection Result", use_column_width=True)

            with col2:
                st.image(mask, caption="Mask", use_column_width=True)
                if hsv_plot:
                    st.image(hsv_plot, caption="HSV Distribution", use_column_width=True)

            st.markdown(get_image_download_link(Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB)), "result.jpg", "Download Result"), unsafe_allow_html=True)

        else:
            selected_colors = st.sidebar.multiselect(
                "Select Colors",
                list(detector.color_presets.keys())[:-1],  # Exclude Custom
                default=["Red", "Green", "Blue"]
            )

            result, all_masks, detection_stats = detector.detect_all_colors(image, selected_colors, params)

            col1, col2 = st.columns(2)

            with col1:
                st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Original Image", use_column_width=True)
                st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), caption="Detection Result", use_column_width=True)

            with col2:
                st.image(all_masks, caption="Combined Masks", use_column_width=True)
                st.write(detection_stats)
    else:
        st.info("Please upload or select an image.")

if __name__ == "__main__":
    main()

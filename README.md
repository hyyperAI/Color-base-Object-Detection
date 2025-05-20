# Multi-Color Object Detection Using HSV Thresholding and Morphological Processing

## Introduction

This project implements a classical image processing pipeline to detect multiple colored objects using HSV color thresholding, morphological operations, and contour analysis. The goal is to accurately identify and classify objects based on their color and shape, with results visualized through an interactive Streamlit-based GUI. The application is robust, modular, and extendable for educational or development purposes.

## Table of Contents

* [Introduction](#introduction)
* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Inputs](#inputs)
* [Methodology](#methodology)
* [Results](#results)
* [Future Scope](#future-scope)
* [Dependencies](#dependencies)
* [Contributors](#contributors)
* [License](#license)

## Features

* Detects multiple colors (Red, Green, Blue, Yellow, Purple) using HSV masking
* Identifies circular vs. non-circular objects using contour shape analysis
* Noise reduction using morphological operations (erosion, dilation)
* GUI interface for interactivity, parameter tuning, and image upload
* Generates downloadable output and HSV scatter plots

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/hyyperAI/Color-base-Object-Detection.git
   cd multi-color-object-detection
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. Upload an image or use the webcam.

3. Adjust HSV thresholds, morphological settings, and minimum contour area via sliders.

4. View detection results, statistical breakdown, and download the processed image.

## Inputs

* **Sample Image 1**: Includes red, green, and blue shapes.
* **Sample Image 2**: Includes red, green, blue, yellow, and purple shapes.
* **User Upload**: Supports image upload or webcam input.

## Methodology

1. **Color Thresholding (HSV)**

   * Image converted to HSV space
   * Color masks created based on preset HSV ranges
   * Handles special cases (e.g., red spans HSV boundaries)

2. **Morphological Operations**

   * Erosion and dilation to clean up noise
   * Adjustable via GUI sliders

3. **Contour Detection and Filtering**

   * Extract contours and remove small/noise contours
   * Compute circularity: `4π * Area / Perimeter²`
   * Circularity > 0.7 is classified as a ball

4. **Visualization and Statistics**

   * Display original, mask, and processed images
   * Show detected object stats in tabular form
   * Generate HSV scatter plot for pixel distribution

## Results

| Color | Circular Objects | Other Objects | Total |
| ----- | ---------------- | ------------- | ----- |
| Red   | 1                | 0             | 1     |
| Green | 1                | 0             | 1     |
| Blue  | 0                | 1             | 1     |

* High accuracy in both color and shape detection
* Resilient to noise due to preprocessing
* Designed for easy modular expansion

## Future Scope

* Add real-time object tracking for video feeds
* Implement adaptive HSV thresholding
* Extend to real-time webcam detection
* Integrate machine learning for object classification

## Dependencies

* Python
* OpenCV (`cv2`)
* NumPy
* PIL (Python Imaging Library)
* Matplotlib
* Streamlit

## Contributors

* Muzammil Khalid (B22F0215AI078)
* Usman Sajid (B22F0590AI121)
  **BS-AI(Green), Supervised by Mr. Rizwan Shah**

## License

This project is for academic and educational use. Please contact the authors for licensing details if required.


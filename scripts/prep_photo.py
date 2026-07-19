import sys
import cv2
import numpy as np
from rembg import remove
from PIL import Image
import os

def prep_photo(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Could not find input image at {input_path}")
        sys.exit(1)
        
    print(f"Loading {input_path}...")
    input_image = Image.open(input_path)
    
    print("Removing background (this might download a model the first time)...")
    no_bg = remove(input_image)
    
    no_bg_cv = cv2.cvtColor(np.array(no_bg), cv2.COLOR_RGBA2BGRA)
    b, g, r, a = cv2.split(no_bg_cv)
    gray = cv2.cvtColor(no_bg_cv, cv2.COLOR_BGRA2GRAY)
    
    print("Enhancing contrast...")
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    white_bg = np.ones_like(enhanced) * 255
    alpha_factor = a.astype(float) / 255.0
    composited = (enhanced * alpha_factor + white_bg * (1 - alpha_factor)).astype(np.uint8)
    
    print(f"Saving prepped photo to {output_path}...")
    cv2.imwrite(output_path, composited)
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <input_image>")
        sys.exit(1)
    
    prep_photo(sys.argv[1], "source-prepped.png")

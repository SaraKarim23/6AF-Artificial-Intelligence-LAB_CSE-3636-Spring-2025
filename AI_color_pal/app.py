from flask import Flask, render_template, request
from PIL import Image
import numpy as np
import cv2
from sklearn.cluster import KMeans
import webcolors
import os

app = Flask(_name_)

# Upload folder
UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Convert RGB to HEX
def rgb_to_hex(color):
    return '#{:02x}{:02x}{:02x}'.format(int(color[0]), int(color[1]), int(color[2]))

# Find closest color name (fallback)
def closest_css3_name(requested_rgb):
    min_distance = float('inf')
    closest_name = None
    for hex_value, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(hex_value)
        distance = (r_c - requested_rgb[0])*2 + (g_c - requested_rgb[1])2 + (b_c - requested_rgb[2])*2
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    return closest_name

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Process image
            image = Image.open(filepath).convert("RGB")
            image_np = np.array(image)
            image_small = cv2.resize(image_np, (200, 200))
            pixels = image_small.reshape(-1, 3)

            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            kmeans.fit(pixels)
            colors = kmeans.cluster_centers_.astype(int)

            # Create palette image
            palette_img = np.zeros((50, 300, 3), dtype='uint8')
            steps = 300 // len(colors)
            for i, color in enumerate(colors):
                start = i * steps
                end = start + steps
                palette_img[:, start:end, :] = color
            palette_path = os.path.join(app.config['UPLOAD_FOLDER'], "palette.png")
            cv2.imwrite(palette_path, cv2.cvtColor(palette_img, cv2.COLOR_BGR2RGB))

            hex_codes = []
            color_names = []

            for color in colors:
                hex_code = rgb_to_hex(color)
                try:
                    name = webcolors.hex_to_name(hex_code, spec='css3')
                except ValueError:
                    name = closest_css3_name(color)
                hex_codes.append(hex_code)
                color_names.append(name)

            return render_template("index.html",
                                   uploaded_image=file.filename,
                                   palette_image="palette.png",
                                   hex_codes=hex_codes,
                                   color_names=color_names)

    return render_template("index.html", uploaded_image=None)

if _name_ == "_main_":
    app.run(debug=True)
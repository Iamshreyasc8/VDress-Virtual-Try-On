from flask import Flask, render_template, request, url_for, abort
import os
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__, template_folder="demo_templates")

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
GRID_FOLDER = 'static/grid_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRID_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # List images from the grid_images folder
    grid_images = sorted(f for f in os.listdir(GRID_FOLDER) if allowed_file(f) and os.path.isfile(os.path.join(GRID_FOLDER, f)))
    return render_template('index.html', grid_images=grid_images)

@app.route('/upload', methods=['POST'])
def upload():
    # Get selected grid image
    selected_image = request.form.get('selected_image')
    selected_image_path = None

    # If a grid image was selected, copy it to the uploads folder
    if selected_image:
        if selected_image != secure_filename(selected_image) or not allowed_file(selected_image):
            abort(400, "Invalid grid image")
        if not os.path.isfile(os.path.join(GRID_FOLDER, selected_image)):
            abort(404, "Grid image not found")
        original_path = os.path.join(GRID_FOLDER, selected_image)
        selected_image_filename = f"selected_{selected_image}"
        selected_image_path = os.path.join(UPLOAD_FOLDER, selected_image_filename)
        shutil.copy(original_path, selected_image_path)

    # Handle uploaded file from local machine
    uploaded_file = request.files.get('uploaded_file')
    uploaded_image_path = None

    if uploaded_file and allowed_file(uploaded_file.filename):
        from uuid import uuid4
        filename = uuid4().hex + "_" + secure_filename(uploaded_file.filename)
        uploaded_image_path = os.path.join(UPLOAD_FOLDER, filename)
        uploaded_file.save(uploaded_image_path)

    # Convert the paths to be relative to the 'static' folder
    selected_image_url = None
    uploaded_image_url = None

    if selected_image_path:
        selected_image_url = url_for('static', filename=f"uploads/{os.path.basename(selected_image_path)}")
    
    if uploaded_image_path:
        uploaded_image_url = url_for('static', filename=f"uploads/{os.path.basename(uploaded_image_path)}")

    return render_template('result.html', 
                           selected_image=selected_image_url, 
                           uploaded_image=uploaded_image_url)

if __name__ == '__main__':
    app.run(debug=False)

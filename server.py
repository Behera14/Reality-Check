from flask import Flask, render_template, redirect, request, url_for, send_file, send_from_directory, flash
from flask import jsonify, json
from werkzeug.utils import secure_filename
import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
os.environ['MEDIAPIPE_DISABLE_GPU']='1'  # Force MediaPipe to use CPU only

# Memory optimization settings
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'
os.environ['VECLIB_MAXIMUM_THREADS'] = '1'

import torch
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
import numpy as np
import cv2
import mediapipe as mp
from torch.autograd import Variable
import time
import uuid
import sys
import traceback
from PIL import Image
# Initialize MediaPipe Face Mesh for CPU
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    refine_landmarks=False  # Disable GPU-dependent feature
)
import logging
import zipfile
from torch import nn
import torch.nn.functional as F
from torchvision import models
from skimage import img_as_ubyte
import warnings
warnings.filterwarnings("ignore")
# Remove matplotlib imports since we're not generating graphs
# import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('Agg')
# from matplotlib.colors import LinearSegmentedColormap
from huggingface_hub import hf_hub_download

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path for the upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Uploaded_Files')
# Remove unused folder paths
# FRAMES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'frames')
# GRAPHS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'graphs')
DATASET_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Admin', 'datasets')

# Create the folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(FRAMES_FOLDER, exist_ok=True)
# os.makedirs(GRAPHS_FOLDER, exist_ok=True)
os.makedirs(DATASET_FOLDER, exist_ok=True)

# Ensure folders have proper permissions
# os.chmod(FRAMES_FOLDER, 0o755)
# os.chmod(GRAPHS_FOLDER, 0o755)
os.chmod(DATASET_FOLDER, 0o755)

video_path = ""
detectOutput = []

app = Flask("__main__", template_folder="templates", static_folder="static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize SQLAlchemy
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create all database tables
with app.app_context():
    db.create_all()

# Dataset comparison accuracies
DATASET_ACCURACIES = {
    'Our Model': None,
    'FaceForensics++': 85.1,
    'DeepFake Detection Challenge': 82.3,
    'DeeperForensics-1.0': 80.7
}

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match")

        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('signup.html', error="Email already exists")

        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('signup.html', error="Username already exists")

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('homepage'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('homepage'))
        else:
            return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

class Model(nn.Module):
    def __init__(self, num_classes, latent_dim=2048, lstm_layers=1, hidden_dim=2048, bidirectional=False):
        super(Model, self).__init__()
        model = models.resnext50_32x4d(pretrained=True)
        self.model = nn.Sequential(*list(model.children())[:-2])
        self.lstm = nn.LSTM(latent_dim, hidden_dim, lstm_layers, bidirectional)
        self.relu = nn.LeakyReLU()
        self.dp = nn.Dropout(0.4)
        self.linear1 = nn.Linear(2048, num_classes)
        self.avgpool = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        batch_size, seq_length, c, h, w = x.shape
        x = x.view(batch_size*seq_length, c, h, w)
        fmap = self.model(x)
        x = self.avgpool(fmap)
        x = x.view(batch_size, seq_length, 2048)
        x_lstm,_ = self.lstm(x, None)
        return fmap, self.dp(self.linear1(x_lstm[:,-1,:]))

def predict(model, img, path='./'):
    try:
        with torch.no_grad():
            fmap, logits = model(img)
            params = list(model.parameters())
            weight_softmax = model.linear1.weight.detach().cpu().numpy()
            logits = F.softmax(logits, dim=1)
            _, prediction = torch.max(logits, 1)
            confidence = logits[:, int(prediction.item())].item() * 100
            logger.info(f'Prediction confidence: {confidence}%')
            return [int(prediction.item()), confidence]
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        traceback.print_exc()
        raise

class validation_dataset(Dataset):
    def __init__(self, video_names, sequence_length=60, transform=None):
        self.video_names = video_names
        self.transform = transform
        self.count = sequence_length

    def __len__(self):
        return len(self.video_names)

    def __getitem__(self, idx):
        video_path = self.video_names[idx]
        frames = []
        a = int(100 / self.count)
        first_frame = np.random.randint(0,a)
        for i, frame in enumerate(self.frame_extract(video_path)):
            # Convert BGR to RGB for MediaPipe Face Mesh
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)
            
            try:
                if results.multi_face_landmarks:
                    face_landmarks = results.multi_face_landmarks[0]
                    
                    # Get face bounding box from landmarks
                    h, w, _ = frame.shape
                    x_coordinates = [landmark.x for landmark in face_landmarks.landmark]
                    y_coordinates = [landmark.y for landmark in face_landmarks.landmark]
                    
                    x_min, x_max = min(x_coordinates), max(x_coordinates)
                    y_min, y_max = min(y_coordinates), max(y_coordinates)
                    
                    # Convert normalized coordinates to pixel coordinates
                    x = int(x_min * w)
                    y = int(y_min * h)
                    face_width = int((x_max - x_min) * w)
                    face_height = int((y_max - y_min) * h)
                    
                    # Add padding (20%)
                    padding_x = int(face_width * 0.2)
                    padding_y = int(face_height * 0.2)
                    
                    # Calculate coordinates with padding and boundary checks
                    left = max(0, x - padding_x)
                    top = max(0, y - padding_y)
                    right = min(w, x + face_width + padding_x)
                    bottom = min(h, y + face_height + padding_y)
                    
                    frame = frame[top:bottom, left:right, :]
            except:
                pass
            frames.append(self.transform(frame))
            if(len(frames) == self.count):
                break
        frames = torch.stack(frames)
        frames = frames[:self.count]
        return frames.unsqueeze(0)

    def frame_extract(self, path):
        vidObj = cv2.VideoCapture(path)
        success = 1
        while success:
            success, image = vidObj.read()
            if success:
                yield image

def detectFakeVideo(videoPath):
    start_time = time.time()
    
    try:
        logger.info(f"Starting video analysis for: {videoPath}")
        
        im_size = 112
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]

        train_transforms = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((im_size,im_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean,std)
        ])
        
        logger.info("Creating video dataset...")
        path_to_videos = [videoPath]
        video_dataset = validation_dataset(path_to_videos, sequence_length=20, transform=train_transforms)
        
        logger.info("Getting model...")
        # Use the lazy-loaded model instead of creating a new one
        model, _ = get_model()
        
        logger.info("Running prediction...")
        prediction = predict(model, video_dataset[0], './')
        
        processing_time = time.time() - start_time
        logger.info(f"Video processing completed in {processing_time:.2f} seconds")
        logger.info(f"Prediction result: {prediction}")
        
        return prediction, processing_time
    except Exception as e:
        logger.error(f"Error in detectFakeVideo: {str(e)}")
        traceback.print_exc()
        raise

def get_datasets():
    datasets = []
    for item in os.listdir(DATASET_FOLDER):
        if item.endswith('.zip'):
            path = os.path.join(DATASET_FOLDER, item)
            stats = os.stat(path)
            datasets.append({
                'name': item,
                'size': stats.st_size,
                'upload_date': datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
    return datasets

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'model_loaded': _model is not None
    })

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/admin')
@login_required
def admin():
    datasets = get_datasets()
    return render_template('admin.html', datasets=datasets)

@app.route('/admin/upload', methods=['POST'])
@login_required
def admin_upload():
    if 'dataset' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})
        
    dataset = request.files['dataset']
    if dataset.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
        
    if not dataset.filename.lower().endswith('.zip'):
        return jsonify({'success': False, 'error': 'Invalid file format. Please upload ZIP files only.'})
        
    try:
        filename = secure_filename(dataset.filename)
        filepath = os.path.join(DATASET_FOLDER, filename)
        dataset.save(filepath)
        
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.testzip()
            
        logger.info(f"Dataset uploaded successfully: {filename}")
        return jsonify({
            'success': True,
            'message': 'Dataset uploaded successfully',
            'dataset': {
                'name': filename,
                'size': os.path.getsize(filepath),
                'upload_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        logger.error(f"Error uploading dataset: {str(e)}")
        return jsonify({'success': False, 'error': f'Error uploading dataset: {str(e)}'})

@app.route('/detect', methods=['GET', 'POST'])
@login_required
def detect():
    if request.method == 'GET':
        return render_template('detect.html')
    if request.method == 'POST':
        try:
            if 'video' not in request.files:
                return render_template('detect.html', error="No video file uploaded")
                
            video = request.files['video']
            if video.filename == '':
                return render_template('detect.html', error="No video file selected")
                
            if not video.filename.lower().endswith(('.mp4', '.avi', '.mov')):
                return render_template('detect.html', error="Invalid file format. Please upload MP4, AVI, or MOV files.")
            
            # Check file size (limit to 100MB)
            video.seek(0, 2)  # Seek to end
            file_size = video.tell()
            video.seek(0)  # Reset to beginning
            
            if file_size > 100 * 1024 * 1024:  # 100MB limit
                return render_template('detect.html', error="File too large. Please upload a video smaller than 100MB.")
                
            video_filename = secure_filename(video.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
            video.save(video_path)
            
            logger.info(f"Processing video: {video_filename} (size: {file_size} bytes)")
            
            # Check if video file exists and has content
            if not os.path.exists(video_path) or os.path.getsize(video_path) == 0:
                raise Exception("Video file is empty or corrupted")
            
            # Process video without signal-based timeout
            prediction, processing_time = detectFakeVideo(video_path)
            
            if prediction is None or len(prediction) < 2:
                raise Exception("Model prediction failed")
            
            if prediction[0] == 0:
                output = "FAKE"
            else:
                output = "REAL"
            confidence = prediction[1]
            
            logger.info(f"Video prediction: {output} with confidence {confidence}%")
            
            data = {
                'output': output, 
                'confidence': confidence,
                'processing_time': round(processing_time, 2)
            }
            
            logger.info(f"Sending response data: {data}")
            data = json.dumps(data)
            
            os.remove(video_path)
            return render_template('detect.html', data=data)
            
        except Exception as e:
            # Clean up video file if it exists
            if 'video_path' in locals() and os.path.exists(video_path):
                os.remove(video_path)
            
            error_msg = str(e)
            logger.error(f"Error processing video: {error_msg}")
            traceback.print_exc()
            
            # Return a more user-friendly error message
            if "timeout" in error_msg.lower():
                return render_template('detect.html', error="Processing took too long. Please try with a shorter video (under 30 seconds).")
            elif "memory" in error_msg.lower():
                return render_template('detect.html', error="Video too large. Please try with a smaller video file.")
            else:
                return render_template('detect.html', error=f"Error processing video: {error_msg}")

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

# ✅ Define DFModel before loading state dict
class DFModel(torch.nn.Module):
    def __init__(self, num_classes=2, latent_dim=2048, lstm_layers=1, hidden_dim=2048, bidirectional=False):
        super(DFModel, self).__init__()
        model = models.resnext50_32x4d(pretrained=True)  # Ensure same base model
        self.model = torch.nn.Sequential(*list(model.children())[:-2])
        self.lstm = torch.nn.LSTM(latent_dim, hidden_dim, lstm_layers, bidirectional)
        self.linear1 = torch.nn.Linear(2048, num_classes)
        self.avgpool = torch.nn.AdaptiveAvgPool2d(1)
        self.dp = torch.nn.Dropout(0.4)

    def forward(self, x):
       # Assuming 'x' is 4D, e.g., [batch_size, channels, height, width]
        x = x.unsqueeze(1)  # Adding sequence length dimension (1 for single image)
        batch_size, seq_length, c, h, w = x.shape
        x = x.view(batch_size * seq_length, c, h, w)
        fmap = self.model(x)
        x = self.avgpool(fmap)
        x = x.view(batch_size, seq_length, 2048)
        x_lstm, _ = self.lstm(x, None)
        return fmap, self.dp(self.linear1(x_lstm[:, -1, :]))

# Lazy loading for model
_model = None
_transform = None

def get_model():
    global _model, _transform
    if _model is None:
        try:
            logger.info("Loading model from Hugging Face Hub...")
            # ✅ Load model from Hugging Face
            model_path = hf_hub_download(repo_id="imtiyaz123/DF_Model", filename="df_model.pt")
            
            # ✅ Initialize model and load weights properly
            _model = DFModel()
            _model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
            _model.eval()
            
            # ✅ Image transformation
            _transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            
            logger.info("Model loaded successfully!")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    return _model, _transform

def predict_image(image_path):
    try:
        model, transform = get_model()
        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0)
        with torch.no_grad():
            _, output_tensor = model(image)  # Get the second element of the tuple (output_tensor)
            probabilities = torch.nn.functional.softmax(output_tensor, dim=1)
            confidence, predicted_class = torch.max(probabilities, 1)
            return int(predicted_class.item()), float(confidence.item()) * 100
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        traceback.print_exc()
        return None, None


@app.route('/image-detect', methods=['GET', 'POST'])
def image_detect():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('image.html', error="No image file uploaded")
        
        image = request.files['image']
        if image.filename == '':
            return render_template('image.html', error="No image file selected")
        
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        
        prediction, confidence = predict_image(image_path)
        
        if prediction is None:
            return render_template('image.html', error="Error processing image")
        
        output = "FAKE" if prediction == 0 else "REAL"
        os.remove(image_path)
        return render_template('image.html', output=output, confidence=confidence)
    
    return render_template('image.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # For Render deployment, bind to 0.0.0.0
    app.run(host="0.0.0.0", port=port, debug=debug, threaded=True)
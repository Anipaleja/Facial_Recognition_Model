# Facial Recognition Model

A powerful and modular deep learning-based facial recognition system for real-time detection, encoding, and identification of human faces. Built with cutting-edge computer vision and neural network techniques, this project is designed for both research and production use-cases including security, attendance tracking, and human-computer interaction.

## Features

- High-accuracy facial **detection** using MTCNN or RetinaFace  
- Facial **embedding/encoding** with models like FaceNet or ArcFace  
- Robust **identification & verification** via vector similarity metrics  
- Real-time webcam/video stream support (OpenCV)  
- Optional **API endpoint** via Flask or FastAPI  
- Optional **liveness detection** to prevent spoofing  
- ROC curve, accuracy, F1-score evaluation  
- Easily extensible with your own dataset  
- GPU acceleration with CUDA / Apple M1 support  

## Project Structure

```bash
facial-recognition-model/
│
├── data/                   # Face images or dataset
├── embeddings/             # Stored face encodings
├── models/                 # Pretrained CNNs (FaceNet, ArcFace, etc.)
├── utils/                  # Utility functions (preprocessing, visualization, etc.)
├── api/                    # Flask or FastAPI server (optional)
├── demo/                   # Jupyter notebooks and test media
├── train.py                # Training script (if applicable)
├── recognize.py            # Main recognition script (webcam or video)
├── requirements.txt
└── README.md
```

## Installation
1. Clone the Repository
```bash
git clone https://github.com/anipaleja/Facial_Recognition_Model.git
cd Facial_Recognition_Model
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

Or with conda:

```bash
conda create -n facereco python=3.8
conda activate facereco
pip install -r requirements.txt
```

3. Download Pretrained Models
Place your pretrained models (e.g. FaceNet, ArcFace .pth or .pb files) in the /models directory. You can use:

- [FaceNet](https://github.com/davidsandberg/facenet)

- [InsightFace](https://github.com/deepinsight/insightface)

## Usage
Run Real-Time Recognition (Webcam):

```bash
python recognize.py --source webcam
```

Recognize From a Video File:
```bash
python recognize.py --source "input_video.mp4"
```
Add New Face to Database:
```bash
python add_face.py --name "Anish"
```

Launch the API (Optional):
```bash
cd api
uvicorn app:app --reload
```

## Evaluation
You can evaluate model performance using ROC curve and classification metrics:

```bash
python evaluate.py --test-data test_dataset/
```

Metrics logged:

- Accuracy

- Precision / Recall

- F1-score

- ROC AUC

## Supported Architectures
### Face Detection:

- MTCNN

- RetinaFace

- Haar Cascades (fallback)

### Face Embedding:

- FaceNet

- ArcFace

- Dlib ResNet

### Liveness Detection (optional):

- Blink Detection (Eye aspect ratio)

- Texture-based CNN

## References
- [FaceNet](https://arxiv.org/abs/1503.03832): A Unified Embedding for Face Recognition and Clustering

- [InsightFace](https://github.com/deepinsight/insightface): 2D and 3D Face Analysis Project

- [MTCNN Face Detector](https://github.com/ipazc/mtcnn)

- [Dlib Face Recognition](https://dlib.net/face_recognition.py.html)

## Author
Anish Paleja - 2025
"Making machines see and understand people."
Email: `anipaleja@gmail.com`
[LinkedIn](https://www.linkedin.com/in/anish-paleja-85b951328/)

## License
This project is licensed under the **MIT License**.

## Acknowledgements
- OpenCV team

- Dlib & DeepInsight contributors

- TensorFlow and PyTorch communities

## Future Roadmap
- On-device iOS/Android support with CoreML / TensorFlow Lite
- Support for face clustering and unsupervised classification
- Integration with home automation or smart door systems
- Improved anti-spoofing via depth + IR sensors

📷 Example Output
```bash
[INFO] Detected: 1 face(s)
[INFO] Recognized: Anish (99.32% match)
[INFO] Face matched with embeddings/anish.npy
```

**Disclaimer:** This tool is intended for educational and ethical use only. Please respect user privacy and comply with all applicable laws.

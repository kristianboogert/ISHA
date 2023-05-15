read -p "Enter the first two digits of the python version you are using [3.10]: " PYTHON_VERSION
PYTHON_VERSION="${PYTHON_VERSION:=3.10}"
echo "Downloading pose_landmark_lite.tflite..."
wget https://storage.googleapis.com/mediapipe-assets/pose_landmark_lite.tflite -O ~/.local/lib/python`echo $PYTHON_VERSION`/site-packages/mediapipe/modules/pose_landmark/pose_landmark_lite.tflite
echo "Downloading hand_landmark_lite.tflite..."
wget https://storage.googleapis.com/mediapipe-assets/hand_landmark_lite.tflite -O ~/.local/lib/python`echo $PYTHON_VERSION`/site-packages/mediapipe/modules/hand_landmark/hand_landmark_lite.tflite
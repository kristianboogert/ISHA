# ISHA

ISHA Minor InHolland

Create CVA appropriate score using computer vision and pose detection.

# Installing dependencies

```bash
python3 -m pip install -r requirements.txt
```

# Downloading the required .tflite model

This project uses an older version of MediaPipe, so it can run on a Raspberry Pi 4. For this reason, it is required to download the model manually. Newer versions of MediaPipe do this automatically.

Execute

```bash
scripts/download_lite_models.bat
```

on Windows or

```bash
scripts/download_lite_models.sh
```

on Linux.

# Usage (pose scoring system)

## Look at a defined exercise description and give a score

The pose scoring system uses a `json` file to score a certain body pose. When a correctly formatted `json` file is given, the body pose is automatically scored.

The pose scoring system can be started as follows:

```bash
python3 src/main.py <description_file.json>
```

## Create a new exercise description by showing how to do an exercise

To add a new body pose to the exercises, a separate python script is created. It looks at the given body pose and creates a `json` file. The generated `json` file can then be used to score an exercise.

```bash
python3 src/createExerciseDescription.py <description_file.json>
```

## Debug/view pose detection data

To debug the pose detection system, a small script is created. It shows the detected heading for the given body parts.

```bash
python3 src/poseDetectionDebugDemo.py
```

# API

## To run local machine

uvicorn api.app.main:app --reload

# ISHA

ISHA Minor InHolland

Create CVA appropriate score using computer vision and pose detection.

# Installing dependencies

```sh
python3 -m pip install -r requirements.txt
```

# Downloading the required .tflite model

This project uses an older version of MediaPipe, so it can be ran on a Raspberry Pi 4. For this reason, it is required to download the model manually. Newer versions of MediaPipe do this automatically.

Execute

```sh
scripts/download_lite_models.bat
```

on Windows or

```bash
scripts/download_lite_models.sh
```

on Linux.

# Running the project

```sh
python3 main.py
```

# To run local machine
uvicorn api.app.main:app --reload

# TODO

- update exerciseCreator so a tracker type is now per body part
- update fugl-meyer class to handle hand tracking
- update exerciseCreator so repeating an exercise is possible
- update fugl-meyer so repeating an exercise is possible
- update exerciseCreator to look at hand rotation
- update fuglMeyer to look at hand rotation

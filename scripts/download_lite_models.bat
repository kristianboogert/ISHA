@echo off
echo THIS SCRIPT ASSUMES YOU ARE USING PYTHON 3.9. IF THIS IS NOT THE CASE, OPEN THIS FILE WITH NOTEPAD AND EDIT THE PYTHON VERSION NUMBER!
echo THIS SCRIPT ALSO ASSUMES YOU HAVE CURL INSTALLED! IT SHOULD COME WITH WINDOWS, BUT MAKE SURE IT IS INSTALLED!
echo THIS SCRIPT ALSO ASSUMES THAT YOU INSTALLED PYTHON VIA `choco install python39`! IF THIS IS NOT TE CASE, OPEN THIS FILE IN NOTEPAD AND EDIT THE TARGET PYTHON PATH!
pause
curl https://storage.googleapis.com/mediapipe-assets/pose_landmark_lite.tflite -o c:\python39\lib\site-packages\mediapipe\modules\pose_landmark\pose_landmark_lite.tflite
curl https://storage.googleapis.com/mediapipe-assets/hand_landmark_lite.tflite -o c:\python39\lib\site-packages\mediapipe\modules\hand_landmark\hand_landmark_lite.tflite

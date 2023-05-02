echo "THIS SCRIPT ASSUMES YOU ARE USING PYTHON 3.9. IF THIS IS NOT THE CASE, OPEN THIS FILE WITH NOTEPAD AND EDIT THE PYTHON VERSION NUMBER!"
echo "THIS SCRIPT ALSO ASSUMES YOU HAVE WGET INSTALLED! IF THIS IS NOT THE CASE, INSTALL IT FIRST!"
echo ""
echo "Press enter to start"
pause
wget https://storage.googleapis.com/mediapipe-assets/pose_landmark_lite.tflite -O c:\python39\lib\site-packages\mediapipe\modules\pose_landmark\pose_landmark_lite.tflite
wget https://storage.googleapis.com/mediapipe-assets/hand_landmark_lite.tflite -O c:\python39\lib\site-packages\mediapipe\modules\hand_landmark\hand_landmark_lite.tflite
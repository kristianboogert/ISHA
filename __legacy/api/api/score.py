from datetime import datetime

def get_timestamp():
    return datetime.now().strftime(("%y-%m-%d %H:%M:%S"))

Score = {
   "name": "Raise arm to side",
   "pose_detection_type": "BODY_POSE",
   "impaired_side": "RIGHT",
   "exercise_parts":[
         {
            "body_part": "LEFT_UPPER_ARM",
            "plane": "xy",
            "angles": [
               {    
               "xy": 23.3,
               "yz": 24.3,
               "xz": 25.3,
               }
            ],
            "score": 2,
            "ms_since_start": 5
         },
         {
            "body_part": "RIGHT_UPPER_ARM",
            "plane": "xy",
            "angles": [
               {    
               "xy": 23.3,
               "yz": 24.3,
               "xz": 25.3,
               }
            ],
            "score": 2,
            "ms_since_start": 5
         }
      ]
   }


def read_all():
    return list(Score.values())
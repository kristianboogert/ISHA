from datetime import datetime

def get_timestamp():
    return datetime.now().strftime(("%y-%m-%d %H:%M:%S"))

Exercise = {
   "id": 34,
   "name": "name",
   "type": "type",
   "description": "description"
   }


def read_all():
    return list(Exercise.values())

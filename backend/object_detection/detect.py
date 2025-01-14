import base64
from flask import jsonify
import torch
import re

class detect:

    """
        detect function:
            loads yolo model and detects what's in the image
        parameter: 
            image
        return:
            the objects detected in the image
    """
    def detect(image):
        model = torch.hub.load('ultralytics/yolov5', 'yolov5x')

        img = image.partition(",")[2]

        with open("objectImage.jpeg", "wb") as fh:
            fh.write(base64.b64decode(img))

        im = "objectImage.jpeg"

        results = model(im)
        res = str(results.pandas().xyxy[0])
        splitted = res.split('name')
        
        print(results.print())

        classes = re.findall(r'[a-zA-Z]+', splitted[1])
        print(classes)
        print(len(classes))

        store = []
        for i in classes:
            if i in store: 
                continue
            else:
                store.append(i)

        return jsonify({'response': store}), 200


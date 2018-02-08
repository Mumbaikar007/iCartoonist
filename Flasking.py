

import io
from flask import Flask, request, Response, send_file
import jsonpickle
import numpy as np
import cv2

import ImageProcessingFlask

# Initialize the Flask application
app = Flask(__name__)


# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    print(r.data)
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....

    img = ImageProcessingFlask.render(img)

    ## build a response dict to send back to client
    ##response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
    ##response = img


    ## encode response using jsonpickle
    ##response_pickled = jsonpickle.encode(response)

    ##_, img_encoded = cv2.imencode('.jpg', img)
    ##print ( img_encoded)

    cv2.imwrite( 'new.jpeg', img)

    _, img_encoded = cv2.imencode('.jpg', img)

    #return "Hello"

    response = {'message': img_encoded.tostring()}
    response_pickled = jsonpickle.encode(response)

    ##response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")
    ##return send_file(io.BytesIO(img), attachment_filename='new.jpeg', mimetype='image/jpeg')

# start flask app
app.run(host="0.0.0.0", port=5000)
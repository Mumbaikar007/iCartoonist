

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
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....

    img = ImageProcessingFlask.render(img)

    # build a response dict to send back to client
    #response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
    #response = img


    # encode response using jsonpickle

    #_, img_encoded = cv2.imencode('.jpg', img)
    #print ( img_encoded)

    cv2.imwrite( 'new.jpeg', img)


    #response_pickled = jsonpickle.encode(response)
    #return Response(response=response_pickled, status=200, mimetype="application/json")
    return send_file( 'new.jpeg', mimetype="image/jpeg", attachment_filename="new.jpeg", as_attachment=True)

# start flask app
app.run(host="0.0.0.0", port=5000)
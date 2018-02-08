
import base64
import numpy as np
import requests
import json
import cv2

addr = 'http://localhost:5000'
test_url = addr + '/api/testd'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('lena.jpeg')
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
#response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
response = requests.post(test_url)

print(response.text)

image = base64.b64decode(json.loads(response.text)['message']['py/b64'])
#image = base64.b64decode(response.content)

img = cv2.imdecode(np.frombuffer(image, np.uint8), 1)
#cv2.formarray
print img
#print(response)
# decode response

#print image
#print json.loads(response.text)['message']['py/b64']

#img = cv2.imread (json.loads(response.text)['message'] + '.jpeg')
cv2.imshow( 'API', img )
cv2.waitKey(0)
cv2.destroyAllWindows()
# expected output: {u'message': u'image received. size=124x124'}

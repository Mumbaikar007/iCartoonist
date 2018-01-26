


import requests
import json
import cv2

addr = 'http://localhost:5000'
test_url = addr + '/api/test'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('lena.jpeg')
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)

print response

#print(response)
# decode response
#print json.loads(response.text)


cv2.imshow( 'API', response.content )
# expected output: {u'message': u'image received. size=124x124'}

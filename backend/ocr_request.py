import json
import base64
import requests
import uuid
import argparse

import time

import grpc
from concurrent import futures
import ocr_request_pb2
import ocr_request_pb2_grpc


headers = {
  'X-OCR-SECRET': "Q0Z3Q3lURUZwV2ZpUWp0YWp1SEJ4UW5hS2xaVm9USG0="
}

Header = {
    "Content-Type": "application/json",
    "X-OCR-SECRET": "Q0Z3Q3lURUZwV2ZpUWp0YWp1SEJ4UW5hS2xaVm9USG0="
}
ocrURL = "https://42cd8d22585e4cb697870d6a1321a642.apigw.ntruss.com/custom/v1/9669/b252ae27e3b0ae9e9c44ffbdec2010e83ac09a9abeaf37887e44bb423adbccdc/general"

def create_body(name, data_format, url):
    uuids = str(uuid.uuid4())
    uuids = "".join(uuids.split("-"))
    res = {
        "version": "v1",
        "requestId": uuids,
        "timestamp": 0,
        "lang": "ko",
        "images": [
            {
                "name": name,
                "format": data_format,
                "url": url
            }
        ]
    }
    return json.dumps(res)
    


request_json = {
    'images': [
        {
            'format': 'png',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}





class ocrApiService(ocr_request_pb2_grpc.ocrApiServiceServicer):  #check
	def goURL(self, request, context):
		#response = requests.request("POST", ocrURL, headers=Header, data = payload, files = image_folder+request.url)
		# image_file = "./uploads/"+request.url
		image_file = "/home/taekyun/8/assignment-4/backend/uploads/"+request.url
		files = [('file', open(image_file,'rb'))]
		
		response = requests.request("POST", ocrURL, headers=headers, data = payload, files = files)
		#response = requests.post(ocrURL,headers=Header ,data = create_body("medium","PNG",request.url)) #request.url
		#req = json.loads(response.text.replace("'","\""))
		#str2 = ""
		#for i in req["images"][0]["fields"]:
		#	str2 += i["inferText"] + " "
		return ocr_request_pb2.ApiResponse2(result=1, response=response.text)
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ocr_request_pb2_grpc.add_ocrApiServiceServicer_to_server(ocrApiService(), server)  #check
    server.add_insecure_port('[::]:8002')    #check
    server.start()
    server.wait_for_termination()
    		
if __name__ == "__main__":
    print("ocr_request")
    serve()
    

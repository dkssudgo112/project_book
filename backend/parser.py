from flask import Flask, request, make_response, session
import json
import base64
import math
import numpy
import argparse
import requests
import uuid
import time
app = Flask(__name__)

"""
Header = {
    "Content-Type": "application/json",
    "X-OCR-SECRET": "Q0Z3Q3lURUZwV2ZpUWp0YWp1SEJ4UW5hS2xaVm9USG0="
}

headers = {
  'X-OCR-SECRET': "Q0Z3Q3lURUZwV2ZpUWp0YWp1SEJ4UW5hS2xaVm9USG0="
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
    
    
image_file = "./uploads/KakaoTalk_20211201_103735132.png"


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

files = [
  ('file', open(image_file,'rb'))
]
"""



@app.route("/", methods=["POST"])
def run_parser():
    try:
        data = json.loads(request.data.decode("utf-8"))
        str2 = ""
        for i in data["images"][0]["fields"]:
            str2 += i["inferText"] + " "
            print(i["inferText"])
        #return make_response(json.dumps(str2, ensure_ascii=False), 200)
        return make_response(str2, 200)
    except Exception as e:
        print(e)
        return make_response("Error", 400)


		
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8001)
    args = parser.parse_args()

    app.run(threaded=True, port=args.port, host=args.host)


    """		
if __name__ == "__main__":
    print("ocr_reqest")
    response = requests.request("POST", ocrURL, headers=headers, data = payload, files = files)
    #response = requests.post(ocrURL,headers=Header ,data = create_body("medium","PNG","https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FZeNhS%2FbtrmyEvTQ2T%2FZcTYnytOS2X3bS8vouzKf1%2Fimg.png" ))
    #print(response.text)
    req = json.loads(response.text.replace("'","\""))
    #print(req)
    #req2 = json.loads(req["images"][0].replace("'","\""))
    #print(req["images"][0]["fields"][0])
    str2 = ""
    for i in req["images"][0]["fields"]:
   	#print(i["inferText"])
   	 str2 += i["inferText"] + " "
    print(str2)
    """

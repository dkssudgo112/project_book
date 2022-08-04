import os
import sys
from flask import Flask, request, make_response, session
import requests

from datetime import timedelta
import json
import uuid
import base64
import redis
import argparse
import grpc

import ocr_request_pb2
import ocr_request_pb2_grpc


def generate_postback_response(text, titles, status_code):
    response = {
        'response_type': 'postback',
        'postback': {
            'text': text,
            'buttons': []
        }
    }
    for title in titles.keys():
        button = {
            'type': 'postback',
            'title': title,
            'payload': titles[title]
        }
        response['postback']['buttons'].append(button)
    return make_response(json.dumps(response, ensure_ascii=False), status_code)

def generate_regular_response(payload, status_code):
    response = {
        'response_type': 'regular',
        'payload': payload
    }
    return make_response(json.dumps(response, ensure_ascii=False), status_code)

def generate_image_response(payload, image_type, status_code):
    response = make_response(payload, status_code)
    response.headers["Content-Type"] = image_type
    return response


#-----------------------------------------------------------------------------------------------------------
# TODO
#-----------------------------------------------------------------------------------------------------------

app = Flask(__name__)


@app.route('/', methods=["POST"])
# login


# image parsing


def base():
    req = json.loads(request.data.decode("utf-8"))
    req_type = request.headers['content-type']
    sender = req["sender"]["id"]
    print(req)     # check the requested text

    # Login, Bank info register
    if req_type == 'text':
        # TODO
        # login -> redis check -> none // return book data
        str1 = req["message"]["text"]
        if "login" in str1:
        	str2 = str1.split(' ')
        	
        return generate_regular_response("Okay", 200)
        
    
    # image URL -> ocr request -> 
    elif req_type == 'image':
        # TODO

        if not redis.exists(sender+"_SSO_cookie") or not redis.exists(sender+"_bankinfo"):
        	return generate_regular_response("plz login / bank", 200)
        str4 = req["payload"]["url"]  #check
        redis.set(sender+"_imageURL",str4)  #check
        
        channel2 = grpc.insecure_channel("143.248.53.120:8002")   #check
        stub2 = ocr_request_pb2_grpc.ocrApiServiceStub(channel2)
        response2 = stub2.LoginKaistSSO(ocr_request_pb2.urlMsg(url=str4))
  	
        raw_text = response2.text #check
  	
        return generate_regular_response("fail", 200)
        
        
        # Send raw text data to the parser and get parsed text data through HTTP.
        #   - response = requests.post("http://parser_ip:parser_port/", data = raw_text.encode('utf-8'))
        # Reply to the chatbot using 'postback' response type
        

    return generate_regular_response("Wrong content-type", 200)





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    host_ip = "143.248.53.120" #143.248.53.120 -> dock, 
    parser.add_argument("--port", default=30001) #30001 -> local test 19001 -> dock
    parser.add_argument("--api_ip", default=host_ip)
    parser.add_argument("--api_port", type=int, default=8003)
    parser.add_argument("--ocr_ip", default=host_ip)
    parser.add_argument("--ocr_port", type=int, default=8002)
    parser.add_argument("--redis_ip", default=host_ip)
    parser.add_argument("--redis_port", type=int, default=6379)
    parser.add_argument("--parser_ip", default=host_ip)
    parser.add_argument("--parser_port", type=int, default=8001)
    args = parser.parse_args()

    redis = redis.Redis(host=args.redis_ip, port=args.redis_port)
    app.run(threaded=True, port=args.port, host='0.0.0.0')
    

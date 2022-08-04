str4 = image_url

channel2 = grpc.insecure_channel("ocr-request-svc:8002") 
stub2 = ocr_request_pb2_grpc.ocrApiServiceStub(channel2)
response2 = stub2.goURL(ocr_request_pb2.urlMsg(url=str4))

raw_text = response2.response
response3 = requests.post("http://parser-svc:8001/", data = raw_text.encode('utf-8'))

if response3.status_code == 200:
	redis.set(session["userid"]+"_data",response3.text)


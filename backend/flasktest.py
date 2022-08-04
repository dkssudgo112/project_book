from posixpath import dirname
from flask import Flask, render_template, request, session, redirect, url_for, send_file
import os
import sys
import requests
from flask_paginate import Pagination, get_page_args #pip install flask-paginate
from datetime import timedelta
import json
import uuid
import base64
import redis
import argparse
import grpc
from werkzeug.utils import secure_filename

import ocr_request_pb2
import ocr_request_pb2_grpc



# session['userid']  => userid
def get_page_data(offset=0, per_page=5, data = []):
    return data[offset: offset + per_page]
     
app = Flask(__name__)
app.secret_key = "102011334455"

#app.config["IMAGE_UPLOADS"] = "/usr/src/app/backend/uploads"
app.config["IMAGE_UPLOADS"] = "/home/taekyun/8/assignment-4/backend/uploads"

@app.route('/', methods=['GET', 'POST'])
def home():
	# session.clear()
	total = 0
	if request.method=='POST':
		userid = request.form.get('userid')
		password = request.form.get('password')

		if(redis.get(userid+"_pw") and redis.get(userid+"_pw").decode('utf-8') == password):
			session['userid'] = userid
			currentUser = redis.get(userid+"_name").decode('utf-8')
			if(redis.exists(currentUser+"_Total")):
				total = int(redis.get(currentUser+"_Total"))
			else:
				total = 0
			page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page') #default 5
			data = []
                        
			datalist = []

			for i in range(total):
				bookTitle=redis.get(currentUser+"_bookTitle"+str(i+1)).decode('utf-8')
				page_2=redis.get(currentUser+"_page"+str(i+1)).decode('utf-8')
				author = redis.get(currentUser+"_author"+str(i+1)).decode('utf-8')
				ocrFinal = ""
				if redis.exists(currentUser+"_ocrFinal"+str(i+1)):
					ocrFinal = redis.get(currentUser+"_ocrFinal"+str(i+1)).decode('utf-8')
				datalist.append(bookTitle)
				datalist.append(page_2)
				datalist.append(author)
				datalist.append(ocrFinal)
				data.append(datalist)
				datalist = []
				
				

				#datalist.append(page_2)
				#datalist.append(author)
				#datalist.append(ocrFinal)
				#data.append(datalist)


			pagination_data = get_page_data(offset = offset, per_page = per_page, data = data)
			pagination = Pagination(page=page, per_page=per_page, total=total) #page -> current page, per_page -> num of data for 1 page
			return render_template('home.html', currentUser=currentUser, users=pagination_data,
							page=page,
							per_page=per_page,
							pagination=pagination,
							total = total)

                       
                          
		else:
			# 비밀번호가 일치하지 않습니다 에러 메세지 띄우기
			return redirect('/login')

	if "userid" in session:
		currentUser = redis.get(session['userid']+"_name").decode('utf-8')
		# return "already login" #next page
		page, per_page, offset = get_page_args(page_parameter='page',
                        								per_page_parameter='per_page') #default 5

		if(redis.exists(currentUser+"_Total")):
			total = int(redis.get(currentUser+"_Total"))
		else:
			total = 0
		data = []
		datalist = []


		for i in range(total):
			bookTitle=redis.get(currentUser+"_bookTitle"+str(i+1)).decode('utf-8')
			page_2=redis.get(currentUser+"_page"+str(i+1)).decode('utf-8')
			author = redis.get(currentUser+"_author"+str(i+1)).decode('utf-8')
			ocrFinal = ""
			if redis.exists(currentUser+"_ocrFinal"+str(i+1)):
				ocrFinal = redis.get(currentUser+"_ocrFinal"+str(i+1)).decode('utf-8')
			datalist.append(bookTitle)
			datalist.append(page_2)
			datalist.append(author)
			datalist.append(ocrFinal)
			data.append(datalist)
			datalist = []
			print(data)
			print(i)


		pagination_data = get_page_data(offset = offset, per_page = per_page, data = data)
		pagination = Pagination(page=page, per_page=per_page, total=total) #page -> current page, per_page -> num of data for 1 page


		return render_template('home.html', currentUser=currentUser, users=pagination_data,
					page=page,
					per_page=per_page,
					pagination=pagination,
					total = total)

	else:
		return render_template('home.html', currentUser="", total = total)

@app.route('/login', methods=['GET', 'POST'])	
def login():
	if request.method=='GET':
		return render_template('login.html')
	else:
		userid = request.form.get('userid')
		password = request.form.get('password')

		if(redis.get(userid+"_pw") and redis.get(userid+"_pw").decode('utf-8') == password):
			session['userid'] = userid
			# return "login success" # next page
			currentUser = redis.get(userid+"_name").decode('utf-8')
			
			#total = 14
			#return render_template('home.html', currentUser=currentUser, total = 14)
			return redirect('/')
		else:
			return redirect('/login')
		
		
@app.route('/register', methods=['GET','POST'])
def register():
	if request.method =='GET':
		return render_template("register.html")
	else:
		userid = request.form.get('userid')
		username = request.form.get('username')
		password = request.form.get('password')
		re_password = request.form.get('re_password')

		if not (userid and username and password and re_password):
			return "모두 입력해주세요"
		elif password != re_password:
			return "비밀번호를 확인해주세요"
		else:
			redis.set(userid+"_name",username)
			redis.set(userid+"_pw",password)
			#session['userid'] = userid			
			return redirect('/')
		return redirect('/')	
		
@app.route('/logout', methods=['GET'])				
def logout():
	session.clear()
	return redirect('/')			
 
@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
	if "userid" in session:
		currentUser = redis.get(session['userid']+"_name").decode('utf-8')
		if request.method == "POST":
			if request.files:
				image = request.files["image"]
				print("hh", image.filename)
				if image.filename != "":
					image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
					print("Upload the image")

					channel2 = grpc.insecure_channel("0.0.0.0:8002")
					stub2 = ocr_request_pb2_grpc.ocrApiServiceStub(channel2)
					response2 = stub2.goURL(ocr_request_pb2.urlMsg(url=image.filename))
					raw_text = response2.response
					response3 = requests.post("http://0.0.0.0:8001/", data = raw_text.encode('utf-8'))

					ocr_result = response3.text

					print("OCR done")
					print(ocr_result)

					redis.set(session['userid']+"_ocr", ocr_result)
					return redirect(url_for('write_after_ocr'))

		return render_template("upload_image.html", currentUser=currentUser)
	else:
		return render_template('login.html')


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)


@app.route("/read",  methods=['GET', 'POST'])
def read():
	if "userid" in session:
		currentUser = redis.get(session['userid']+"_name").decode('utf-8')
		my_var = request.args.get('my_var', None) #numbering_of_book
		
		
		bookTitle=redis.get(currentUser+"_bookTitle"+str(my_var)).decode('utf-8')
		author=redis.get(currentUser+"_author"+str(my_var)).decode('utf-8')
		date=redis.get(currentUser+"_date"+str(my_var)).decode('utf-8')
		page=redis.get(currentUser+"_page"+str(my_var)).decode('utf-8')
		thought=redis.get(currentUser+"_thought"+str(my_var)).decode('utf-8')
		ocrFinal = ""
		if redis.exists(currentUser+"_ocrFinal"+str(my_var)):
			ocrFinal = redis.get(currentUser+"_ocrFinal"+str(my_var)).decode('utf-8')
		
		print(my_var)
		return render_template('read.html', currentUser=currentUser,ocrFinal=ocrFinal, bookTitle=bookTitle,author=author,date=date,page=page,thought=thought)
	else:
		return render_template('login.html')		

@app.route("/write-after-ocr",  methods=['GET', 'POST'])
def write_after_ocr():
	if "userid" in session:
		currentUser = redis.get(session['userid']+"_name").decode('utf-8')
		ocr_result=""
		if (redis.exists(session['userid']+"_ocr")):
			ocr_result = redis.get(session['userid']+"_ocr").decode('utf-8')
		bookTitle=""
		author=""
		date=""
		page=""
		ocrFinal=""
		thought=""

		if request.method == 'POST':
			bookTitle = request.form.get("bookTitle")
			author = request.form.get("author", "")
			date = request.form.get("date")
			page = request.form.get("page")
			ocrFinal = request.form.get("ocrFinal")
			if ocrFinal is None:
				print(ocrFinal)
			else:
				print('yeyyyyyy')
			thought = request.form.get("thought")
			
			if(redis.exists(currentUser+"_Total") != 1):
				redis.set(currentUser+"_Total",1)
			else:
				redis.incr(currentUser+"_Total",1)

			book_num = int(redis.get(currentUser+"_Total"))
			print("what is book num" + str(book_num))
			
			redis.set(currentUser+"_bookTitle"+str(book_num),bookTitle)
			redis.set(currentUser+str(book_num),bookTitle)
			redis.set(currentUser+"_author"+str(book_num),author)
			redis.set(currentUser+"_date"+str(book_num),date)
			redis.set(currentUser+"_page"+str(book_num),page)
			if ocrFinal is not None:
				redis.set(currentUser+"_ocrFinal"+str(book_num),ocrFinal)
			redis.set(currentUser+"_thought"+str(book_num),thought)

			print(bookTitle, author, date, page, ocrFinal, thought)
			redis.set(session['userid']+"_ocr", "")
			return redirect('/')
			

		return render_template('write_after_ocr.html', currentUser=currentUser, ocr_result=ocr_result)

	else:
		return render_template('login.html')

if __name__ == "__main__":
	redis = redis.Redis(host="0.0.0.0", port=6379)
	# for local test
	# redis = redis.Redis(host="0.0.0.0", port=6379)
	# app.run()
	app.run(debug=True, host='0.0.0.0', port=5000)
# ngrok http 5000

# redis-cli -p 6379
# get all keys : KEYS *
    
    
    
# key : userid_booklist
# value : ['어린왕자_생텍쥐페리', '푸른꽃_작가', '경제_작가']

# key : 어린왕자_생텍쥐페리
# value : [1, 4, 5]

# key : userid_bookname_author
# value : [ocr_data@%date@%thought]

# key : userid_bookname_author_1
# value : [ocr_data@%date@%thought]

# total : 책 개수
# key : userid_1_bookname
# key : userid_1_author
# key : userid_1_date
# key : userid_1_bookname
# key : userid_1_bookname

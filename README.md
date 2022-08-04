# Assignment 4

- Student ID: 20140150, 20160272
- Your Name: 김태균, 박지윤
- Submission date and time: 21-12-09-04:35

## Ethics Oath
I pledge that I have followed all the ethical rules required by this course (e.g., not browsing the code from a disallowed source, not sharing my own code with others, so on) while carrying out this assignment, and that I will not distribute my code to anyone related to this course even after submission of this assignment. I will assume full responsibility if any violation is found later.

Name: ___김태균, 박지윤___ 
Date: ___2021.12.01___


## Brief overview

An interactive reading service that parses text using book photos and leaves notes with notes 


## How to run project
### Install
```
$ git clone https://gitlab.ee324.kaist.ac.kr/20160272/assignment-4.git
$ minikube start
$ docker build -f Dokerfile -t bookgam .
$ kubectl create -f k8s/
$ ngrok http 30001
```  
Open ngrok ~~

## Detailed description
### How to Use 
1. home:  There is a path where you can log in, register, read data, and write data.
2. Register(ID, PW, name)
3. Login
4. uploads image & data
5. You can view the saved data by clicking the saved data list in Home.


## Technology stack
This project consists of a flask-based backend and an html + css frontend.

- flask : flasktest.py(main program), parser.py(ocr data parse program)
   - Implementation of pagination, image source storage, and user data storage through sessions

- html, css: home.html, login.html etc (using with falsk)
   - Nice UI configuration and designed to be usable as a mobile phone

- http, grpc: Protocol used for communication between programs

- ngrok : program that allows external access to a specific port on the server.

- Docker + kubelet : To provide containers and microarchitecture services that run programs

- redis : user database

- Naver OCR : Process the image source saved by the user as an image

## Structures

- flaktest.py: Act as main server
- ocr_request.py: Receive data by communicating with Naver API
- parser.py: Parses the data received from Naver API and sends the desired text
  
  
## Detailed description of the main server

1. How to connect flask and html
```
@app.route('/', methods=['GET', 'POST'])
def home():
~~
	return render_template('home.html',currentUser=currentUser,users=pagination_data,page=page,per_page=per_page,pagination=pagination,total = total)

```

2. Pagination implementation
```
def get_page_data(offset=0, per_page=5, data = []):
    return data[offset: offset + per_page
pagination_data = get_page_data(offset = offset, per_page = per_page, data = data)
pagination = Pagination(page=page, per_page=per_page, total=total)
```

3. User data storage method
```
bookTitle = request.form.get("bookTitle")
redis.set(currentUser+"_bookTitle"+str(book_num),bookTitle)
```

4. image storage knowledge
```
image = request.files["image"]
image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
send_from_directory(app.config["IMAGE_UPLOADS"], filename)
```

5. move data between html
```
<h3><a onclick="location.href='/upload-image'">작성하기</a></h3>
or
<td><a href="{{ url_for('read', my_var=loop.index + (page - 1) * per_page) }}"> {{ user[0] }} Title </a></td>

```



## Credits
- grpc guide: https://developers.google.com/protocol-buffers/docs/pythontutorial
- 네이버 ocr api: https://guide.ncloud-docs.com/docs/ocr-ocr-1-4

## License

 MIT License   

Copyright (c) 2021 Jiyun Park
     
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
     
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
     
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


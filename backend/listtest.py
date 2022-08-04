from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args #pip install flask-paginate
 

 
def get_page_data(offset=0, per_page=5, data = []):
    return data[offset: offset + per_page]
  
app = Flask(__name__)

 
@app.route('/')
def list():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page') #default 5
    total = 14 #number of data
    data = ["i am","babo","no","thankyou","sry","good","yoda","hihi","byebye","keyey","now","end","but","real"] #data query
    pagination_data = get_page_data(offset = offset, per_page = per_page, data = data)
    pagination = Pagination(page=page, per_page=per_page, total=total) #page -> current page, per_page -> num of data for 1 page
    return render_template('list.html',
                           users=pagination_data,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )
 
 
if __name__ == '__main__':
    app.run(debug=True)

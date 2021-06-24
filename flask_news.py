'''
Author: your name
Date: 2021-06-21 15:13:18
LastEditTime: 2021-06-23 18:54:22
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /flask_news/flask_news.py
'''

import re
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import base.methods as METHODS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@ying5319106@localhost:3306/flask_news?charset=utf8'
db = SQLAlchemy(app)

app.debug = True
app.templates_auto_reload = True


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    types = db.Column(db.String(10), nullable=False)
    image = db.Column(db.String(300))
    author = db.Column(db.String(20))
    view_count = db.Column(db.Integer)
    create_at = db.Column(db.DateTime)
    is_valid = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Name %r>' % self.title

    pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cat/<name>')
def cat(name):
    return render_template('cat.html', name=name)


@app.route('/detail/<id>')
def detail(id=''):
    data = News.query.get(id)
    if data:
        return render_template('detail.html', detailData=data)
    else:
        return render_template('404.html')


# 请求数据
@app.route('/query', methods=["POST"])
def query():
    if request.method == 'POST':
        news_list = News.query.filter_by(is_valid=1).all()
        print('jieguo================')
        value = METHODS.toDict(news_list)
        print(value)

        return {
            "status": True,
            "value": value
        }
    else:
        return {
            "status": False,
            "value": None
        }
    pass


@app.route('/add')
def add():
    return render_template('add.html')


# 添加数据
@app.route('/add_data', methods=["POST"])
def add_data():
    if request.method == "POST":
        # 处理请求入参
        reqData = request.get_data()
        reqDict = json.loads(reqData)
        print(reqDict)
        n = News(
            title=reqDict.get("title") or "",
            content=reqDict.get("content") or "",
            types=reqDict.get("types") or "",
            image=reqDict.get("image") or "",
            is_valid=True
        )
        db.session.add(n)
        db.session.commit()
        return {
            "status": True,
        }
    else:
        return {
            "status": False,
        }


# 查详情数据
@app.route('/detail.do', methods=["POST"])
def queryDetail():
    if request.method == "POST":
        try:
            # 处理请求入参
            reqData = request.get_data()
            reqDict = json.loads(reqData)
            print(reqDict)
            news_list = News.query.filter_by(id=reqDict.get('id')).all()
            value = METHODS.toDict(news_list)
            # return redirect(url_for('detail'))
            return {
                "status": True,
                "value": value[0]
            }
        except ValueError:
            print(ValueError)
            return {
                "status": False,
            }
    else:
        return {
            "status": False,
        }


if __name__ == '__main__':
    app.run(debug=True)

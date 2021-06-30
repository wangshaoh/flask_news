'''
Author: wangshaoh
Date: 2021-06-21 15:13:18
LastEditTime: 2021-06-23 18:54:22
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /flask_news/flask_news.py
'''

import re
from flask import Flask, render_template, request, url_for, redirect, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import json
import base.methods as METHODS
import os
import glob

# from werkzeug import security

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@ying5319106@localhost:3306/flask_news?charset=utf8'
app.config['UPLOAD_FOLDER'] = 'upload_flask/'  # 上传文件路径

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


# ==============================页面路由====================================

@app.route('/')
def entry():
    return redirect(url_for('index'))


@app.route('/index')
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


@app.route('/add')
def add():
    return render_template('add.html')


# 文件下载页面
@app.route('/download')
def download():
    fileList = []
    for filename in glob.glob('upload_flask/*'):
        fileList.append(filename[13:])
    print(fileList)
    return render_template('download.html', fileList=fileList)


# ======================================================================================

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


# 删除数据
@app.route('/delete.do', methods=["POST"])
def deleteData():
    if request.method == "POST":
        try:
            # 处理请求入参
            reqData = request.get_data()
            reqDict = json.loads(reqData)
            curData = News.query.get(reqDict.get('id'))
            if curData:
                curData.is_valid = False
                db.session.add(curData)
                db.session.commit()
                return {
                    "status": True
                }
            else:
                return {
                    "status": False,
                    "msg":"未找到该数据"
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


# 文件上传
@app.route('/uploader', methods=["GET", "POST"])
def uploader():
    if (request.method == "POST"):
        f = request.files['file']
        print(request.files)
        print(os.path)
        pt = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(pt)
        return {
            "status": True,
        }
    else:
        return {
            "status": False,
        }


# 文件下载
@app.route('/download.do/<filename>')
def downloadDo(filename):
    if (filename):
        dirpath = os.path.join(app.root_path,
                               'upload_flask')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
        return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载
    else:
        return {
            "status": False,
        }


if __name__ == '__main__':
    app.run(debug=True)

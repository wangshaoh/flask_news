# flask_news


_1、安装flask和flask_sqlalchemy：_

`sudo pip3 install Flask`

`sudo pip3 install flask_sqlalchemy`

_2、在flask_news.py配置自己的mysql数据库_

`app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@ying5319106@localhost:3306/flask_news?charset=utf8'
`

_并且初始化数据库表字段_

`运行python3 环境`

`>>> from flask_news import db`

`>>> db.create_all()`

_3、启动flask调试状态：_

`运行python3 环境`

`$ export FLASK_APP=flask_news.py`

`$ export FLASK_DEBUG=1`

`$ python3 -m flask run`

_或者_

`// ⚠️必须放在文件最底部`

`if __name__ == '__main__': 
    app.run(debug=True)`
    
`$ python3 flask_news.py   ` 

_4、访问 http://127.0.0.1:5000/_ 

_可以切换不同页面
如新增：http://127.0.0.1:5000/add_

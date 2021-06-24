'''
Author: your name
Date: 2021-06-23 18:13:07
LastEditTime: 2021-06-23 18:59:49
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /flask_news/base/methods.py
'''

# 数据转为字典
def toDict(data):
    res = []
    print(data)
    for item in data:
        d = {}
        print(item)
        for key in item.__dict__.keys():
            if(key != "_sa_instance_state"):
                d[key] = item.__dict__[key]
        res.append(d)
    return res
 
    
BASE_METHODS = {
    toDict
}

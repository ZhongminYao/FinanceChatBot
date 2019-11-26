from pymongo import MongoClient
import urllib.parse
import datetime

Authdb='FinanceChatBot'


def constructor():
    client = MongoClient("mongodb://dickyao98:Win19980714!@financechatbot-shard-00-00-q2kn9.mongodb.net:27017,financechatbot-shard-00-01-q2kn9.mongodb.net:27017,financechatbot-shard-00-02-q2kn9.mongodb.net:27017/test?ssl=true&replicaSet=FinanceChatBot-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client[Authdb]
    return db
   

def write_user_stock_fountion(stock, bs, price):  
    db=constructor()
    collect = db['StockDB']
    collect.insert({"stock": stock,
                    "data": 'care_stock',
                    "bs": bs,
                    "price": float(price),
                    "date_info": datetime.datetime.utcnow()
                    })
    

def delete_user_stock_fountion(stock):  
    db=constructor()
    collect = db['StockDB']
    collect.remove({"stock": stock})
    

def show_user_stock_fountion():  
    db=constructor()
    collect = db['StockDB']
    cel=list(collect.find({"data": 'care_stock'}))
    return cel




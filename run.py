#coding:utf-8
from app import app
import count


if __name__ == "__main__":
    #count.cont()
    app.run(debug = True,port= 8082)
    #count.spider()
    #count.myget()
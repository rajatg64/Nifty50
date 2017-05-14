import cherrypy
import random
import json
from urllib.request import urlopen
import urllib
from redisworks import Root
import os
from mako.template import Template
import threading

class Nifty50(object):
    def getData(self):
        url = 'https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json'
        req = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        jsondata = json.loads(html)
        #code to get different color for tiles
        list = []
        tempList=[]
        for i in range(10):
            for j in range(10):
                num=random.randrange(4)
                if tempList.count(num)<3:
                    tempList.append(num)
                    x=num
                    break
            if x == 1:
                list.append('green-tile')
            elif x == 2:
                list.append('red-tile')
            elif x == 3:
                list.append('orange-tile')
            else:
                list.append('purple-tile')

        jsondata['list']=list
        #storing data into rediswork instance
        root=Root()
        root.data=jsondata
        #this thread will get executed after every 5  min
        threading.Timer(300.0, self.getData).start()
        return root

    @cherrypy.expose
    def index(self):
        root=self.getData()
        output=Template(filename="data.html").render(data=root.data)
        return output

# Assumes the config file is in the directory as the source.
conf_path = os.path.dirname(os.path.abspath(__file__))
conf_path = os.path.join(conf_path, "Proj.conf")
cherrypy.config.update(conf_path)
cherrypy.quickstart(Nifty50())

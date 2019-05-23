#-*- coding: UTF-8 -*- 
import web
#import utils

urls = (
	'/','index'
)
app1=web.application(urls,globals())

class index:
	def GET(self):
		greeting = "hello word"
		return greeting
if __name__ == "__main__":
	app1.run()
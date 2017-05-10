from django.http import JsonResponse
import os
import json

def key_exist(func):
	def checkAccessKey(request,*args,**kwargs):
		FILE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		accessKeyFile = open(FILE_DIR+"/metadata/accessKeyList.txt","r")
		accessKeyList = accessKeyFile.read()
		accessKeyFile.close()
		accessKeyList = accessKeyList.strip('\n').split('\n')
		key = ""
		methods = ['POST','PATCH','DELETE']
		if(request.method=='GET'):
			key = str(request.GET['key'])
			print(key,"[==GET==]")
		elif request.method in methods:
			key = json.loads(request.body.decode('utf-8'))['key']
			print(key,request.method)
		else:
			return JsonResponse({"error":True,"description":"Request type did not match"})
		if key not in accessKeyList:
			return JsonResponse({"error":True,"description":"Key not found."})
		else:
			return func(request,*args,**kwargs)
	return checkAccessKey
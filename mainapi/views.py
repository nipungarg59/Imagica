from django.shortcuts import render
from django.http import JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
from .myOwnDecorators import *
import json
import base64

FILE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DETAILS_DIR = FILE_DIR + "/metadata/details"
STATIC_DIR = FILE_DIR + "/djreact/static/images"

def getDebugState():
	if(str(os.environ.get('Debug'))==str(False)):
		return False
	return True

def generateAccessKey(request):
	# print(FILE_DIR)
	accessKeyFile = open(FILE_DIR+"/metadata/accessKeyList.txt","r")
	accessKeyList = accessKeyFile.read()
	accessKeyFile.close()
	accessKeyList = accessKeyList.strip('\n').split('\n')
	# print(accessKeyList)
	newKey = ""
	while True:
		newKey = ""
		for i in range(15):
			from random import randint
			newKey+=chr(randint(97,97+25))
		if newKey not in accessKeyList:
			accessKeyFile = open(FILE_DIR+"/metadata/accessKeyList.txt","a+")
			accessKeyFile.write(newKey+"\n")
			break
	if not os.path.exists(DETAILS_DIR):
		os.makedirs(DETAILS_DIR)
	ff = open(DETAILS_DIR+"/"+newKey+".txt","w")
	ff.close()
	return JsonResponse({"error":False,"accessKey":newKey})


def readImageFile(key):
	detailsOfFile = {}
	IMAGE_FILE_DIR = DETAILS_DIR + "/" + key + ".txt"
	filePtr = open(IMAGE_FILE_DIR,"r")
	fileData = filePtr.read()
	filePtr.close()
	fileData = fileData.strip('\n').split('\n')
	# print(fileData)
	detailsOfFile['count']=0
	detailsOfFile['images'] = []
	for image in fileData:
		if image!='':
			detailsOfFile['count']+=1
			imageDetail = {}
			image = image.split(' ')
			imageDetail['name'] = image[0]
			imageDetail['location'] = image[1]
			imageDetail['partial-url'] = image[2]
			if getDebugState():
				imageDetail['http-url'] = "127.0.0.1:8000"+image[2]
			else:
				imageDetail['http-url'] = "https://imagicaa.herokuapp.com"+image[2]
			detailsOfFile['images'].append(imageDetail)
	return detailsOfFile

def getImageData(key,iname):
	imageDetails = {}
	IMAGE_FILE_DIR = DETAILS_DIR + "/" + key + ".txt"
	filePtr = open(IMAGE_FILE_DIR,"r")
	fileData = filePtr.read()
	filePtr.close()
	fileData = fileData.strip('\n').split('\n')
	# print(fileData)
	imageDetails['exists'] = False
	for image in fileData:
		if image!='':
			image = image.split(' ')
			if(image[0]==iname):
				imageDetails['exists'] = True
				imageDetails['name'] = image[0]
				imageDetails['location'] = image[1]
				if getDebugState():
					imageDetails['http-url'] = "127.0.0.1:8000"+image[2]
				else:
					imageDetails['http-url'] = "https://imagicaa.herokuapp.com"+image[2]
				imageDetails['partial-url'] = image[2]
	return imageDetails

def compressImage(image):
	pass

def addNewImageInFile(key,name,location):
	with open(DETAILS_DIR+'/'+key+'.txt',"a") as file:
		file.write(name+" "+location+" "+"/static/images/"+key+"/"+name+"\n")


def addNewImage(key,data):
	name = data['iname']
	if not os.path.exists(STATIC_DIR+"/"+key):
		os.makedirs(STATIC_DIR+"/"+key)
	CURR_KEY_DIR = STATIC_DIR+"/"+key
	with open(CURR_KEY_DIR + "/" + data['iname'],"wb") as image:
		image.write(base64.decodestring(data['icode']))
	addNewImageInFile(key,data['iname'],data['location'])
	compressImage(CURR_KEY_DIR + "/" + data['iname'])

def deleteImage(key,name):
	IMAGE_FILE_DIR = DETAILS_DIR + "/" + key + ".txt"
	with open(IMAGE_FILE_DIR,"r") as file:
		fileData = file.read()
	fileData = fileData.strip('\n').split('\n')
	# print(fileData)
	file = open(IMAGE_FILE_DIR,"w")
	imageDetails = {}
	for imagee in fileData:
		if imagee!='':
			image = imagee.split(' ')
			if(image[0]==name):
				imageDetails['iname'] = image[0]
				imageDetails['location'] = image[1]
				with open(STATIC_DIR+"/"+key+"/" + name,"rb") as im:
					imageDetails['icode'] = base64.encodestring(im.read())
				os.remove(STATIC_DIR+"/"+key+"/" + name)
			else:
				file.write(imagee+"\n")
	file.close()
	# print(imageDetails)
	return imageDetails



@csrf_exempt
@key_exist
def ImageApi(request):
	dataToBeReturned = {}
	dataToBeReturned['error'] = False
	if(request.method=='GET'):
		key = str(request.GET['key'])
		queryType = str(request.GET['type'])
		dataToBeReturned['accessKey'] = key
		if(queryType=='list'):
			imageFileData = readImageFile(key)
			dataToBeReturned['count'] = imageFileData['count']
			dataToBeReturned['images'] = imageFileData['images']
		elif(queryType=='detail'):
			imageData = getImageData(key,str(request.GET['iname']))
			if imageData['exists']:
				for k in imageData:
					if k!='exists':
						dataToBeReturned[k]=imageData[k]
			else:
				dataToBeReturned['error'] = True
				dataToBeReturned['description'] = "Image does not exists."
		else:
			return JsonResponse({"error":True,"description": "Invalid Query type"})
		# print(key,"[==GET==]")
	else:
		data = json.loads(request.body.decode('utf-8'))
		key = data['key']
		imageData = getImageData(key,str(data['iname']))
		if request.method=='POST':
			if imageData['exists']:
				dataToBeReturned['error'] = True
				dataToBeReturned['description'] = "Image Name Already exists."
			else :
				try:
					if(data['icode'][:4]=="data"):
						s = ""
						found = False
						for i in data['icode']:
							if found:
								s+=i
							elif i==',':
								found=True
						data['icode'] = s
					data['icode'] = data['icode'].encode()
				except :
					pass
				addNewImage(key,data)
		else :
			if not imageData['exists']:
				dataToBeReturned['error'] = True
				dataToBeReturned['description'] = "Image does not exists."
			elif request.method=='PATCH':
				detailsOfImage = deleteImage(key,data['iname'])
				if data['updateAttr']=="icode":
					try:
						data['updateVal'] = data['updateVal'].encode()
					except :
						pass
				detailsOfImage[data['updateAttr']] = data['updateVal']
				addNewImage(key,detailsOfImage)
			elif request.method=="DELETE":
				detailsOfImage = deleteImage(key,data['iname'])
	return JsonResponse(dataToBeReturned)
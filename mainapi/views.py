from django.shortcuts import render
from django.http import JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
from .myOwnDecorators import *
import json

FILE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DETAILS_DIR = FILE_DIR + "/metadata/details"


def generateAccessKey(request):
	print(FILE_DIR)
	accessKeyFile = open(FILE_DIR+"/metadata/accessKeyList.txt","r")
	accessKeyList = accessKeyFile.read()
	accessKeyFile.close()
	accessKeyList = accessKeyList.strip('\n').split('\n')
	print(accessKeyList)
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
	print(fileData)
	detailsOfFile['count']=0
	detailsOfFile['images'] = []
	for image in fileData:
		if image!='':
			detailsOfFile['count']+=1
			imageDetail = {}
			image = image.split(' ')
			imageDetail['name'] = image[0]
			imageDetail['location'] = image[1]
			imageDetail['http-url'] = image[2]
			imageDetail['partial-url'] = image[3]
			detailsOfFile['images'].append(imageDetail)
	return detailsOfFile

def getImageData(key,iname):
	imageDetails = {}
	IMAGE_FILE_DIR = DETAILS_DIR + "/" + key + ".txt"
	filePtr = open(IMAGE_FILE_DIR,"r")
	fileData = filePtr.read()
	filePtr.close()
	fileData = fileData.strip('\n').split('\n')
	print(fileData)
	imageDetails['exists'] = False
	for image in fileData:
		if image!='':
			image = image.split(' ')
			if(image[0]==iname):
				imageDetails['exists'] = True
				imageDetails['name'] = image[0]
				imageDetails['location'] = image[1]
				imageDetails['http-url'] = image[2]
				imageDetails['partial-url'] = image[3]
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
		if request.method=='POST':
			pass
		elif request.method=='PATCH':
			pass
		elif request.method=="DELETE":
			pass
	return JsonResponse(dataToBeReturned)
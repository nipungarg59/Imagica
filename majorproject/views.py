from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def getAnalysis(request):
	data = json.loads(request.body.decode('utf-8'))
	_str_1 = data['phrase_1']
	_str_2 = data['phrase_2']

	response = {
		'result' : True,
		'message' : 'C** banayenge'
	}

	return JsonResponse(response)
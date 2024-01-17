import os, sys, time, json, openai
sys.path.append("/Users/parkjiyoung/Desktop/computer/git/dapphago/back")
from RAG import Rag

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render



def board(request):
    return render(request, 'board/main_board.html')


@csrf_exempt
def get_bot_response(request):
    print(request.POST['question'])
    user_query = request.POST['question']
    rag = Rag()
    response = rag.gpt_api(user_query, 5)
    print(response)
    return JsonResponse({'response': response})

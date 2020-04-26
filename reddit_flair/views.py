from django.shortcuts import render

import json
from django.shortcuts import render, HttpResponse
from django.conf import settings
import sys
import sklearn
import pickle
import praw
import re
from joblib import load
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RedditPost
from .serializers import RedditPostSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RedditPost
from .serializers import RedditPostSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



reddit = praw.Reddit(client_id = "0hliVZBlDhlipQ",client_secret = "pjUJDMMXhYaEmyJaLkQYb_2Fccg",user_agent = "Reddit Flair Detector",username = "chandan21121998",password = "Chandan@1234")


REPLACE_BY_SPACE_RE = re.compile('[/(){}\\[\\]\\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
try:
  model = load('flair_predict.joblib') 
except: 
  model = settings.MODEL_FILE

@api_view(['GET', 'POST'])
def post_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        posts = RedditPost.objects.all()
        serializer = RedditPostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RedditPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            result = utils.predictutil(serializer.data['upload_file'])
            if not result:
                return Response({}, status=status.HTTP_201_CREATED)
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
def clean_text(text):
   
    text = text.lower()
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    return text


def detect_flair(url,loaded_model):

  submission = reddit.submission(url=url)

  data = {}

  data['title'] = submission.title
  data['url'] = submission.url

  submission.comments.replace_more(limit=None)
  comment = ''
  for top_level_comment in submission.comments:
    comment = comment + ' ' + top_level_comment.body
  data["comment"] = comment
  data['title'] = clean_text(data['title'])
  data['comment'] = clean_text(data['comment'])
  data['body'] = submission.selftext
  data['body'] = clean_text(data['body'])
  data['combined'] = data['title'] + data['body'] + data['comment']

  
  return loaded_model.predict([data['combined']])



def predict(request):
    
    if request.method == 'POST':
        
        val = request.POST.get('url')
        return render(request,"flair_detection/main.html",{"output":detect_flair(val,model)[0]})

    return render(request,"flair_detection/main.html")

# Create your views here.

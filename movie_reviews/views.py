from django.shortcuts import render
from django.http import JsonResponse
from django.template import loader

import json
import requests

from .settings import API_KEY
from bookmarks.models import Bookmark, Folder

from django.views.generic import TemplateView

def map_bookmarks_to_articles(array):
  articles = array
  
  links = []
  for article in articles:
    links.append(article['link']['url'])

  bookmarks = Bookmark.objects.filter(link__in=links)

  link = ""
  bookmark = {}

  for article in articles:
    link = article['link']['url']
    bms = bookmarks.filter(link=link)
    if bms.exists():
      article['bookmark_id'] = bms[0].pk

  return articles

def index(request):
  bookmarks = []

  request.session['index'] = 0
  request.session['offset'] = 0

  requestUrl = 'https://api.nytimes.com/svc/movies/v2/reviews/all.json?offset=0&order=by-publication-date&api-key='+API_KEY
  requestHeaders = {
    'Accept': 'application/json'
  }
  
  response = requests.get(requestUrl, headers=requestHeaders)
  content = json.loads(response.content)
  articles = content['results'][0:10]

  if request.user.is_authenticated:
    articles = map_bookmarks_to_articles(articles)

  return render(
    request, 'index.html',
    {'articles': articles, 'counter': 0})


def load_articles(request):
  request.session['index'] = request.session.get('index') + 10
  current_index = request.session.get('index')

  if current_index % 20 == 0:
    request.session['offset'] = request.session.get('offset') + 20

  current_offset = request.session.get('offset')

  requestUrl = 'https://api.nytimes.com/svc/movies/v2/reviews/all.json?'\
    'offset='+str(current_offset)+'&order=by-publication-date&api-key='+API_KEY

  requestHeaders = {
    'Accept': 'application/json'
  }

  response = requests.get(requestUrl, headers=requestHeaders)
  content = json.loads(response.content)
  articles = content['results'][(current_index%20):(current_index+10)%21]

  if request.user.is_authenticated:
    articles = map_bookmarks_to_articles(articles)

  article_html = loader.render_to_string(
    'article.html',
    {'articles': articles, 'user': request.user, 'counter': current_index},
    request=request
  )

  output_data = {
    'article_html': article_html
  }

  return JsonResponse(output_data)


def search_articles(request):
  output_data = {}

  request.session['index'] = 0
  request.session['offset'] = 0
  search_query = ''

  if request.GET:
    search_query = request.GET['search']

  requestUrl = 'https://api.nytimes.com/svc/movies/v2/reviews/search.json?'\
    'offset=0&query='+search_query+'&api-key='+API_KEY
  requestHeaders = {
    "Accept": "application/json"
  }

  response = requests.get(requestUrl, headers=requestHeaders)
  content = json.loads(response.content)
  articles = content['results'][0:10]

  if request.user.is_authenticated:
    articles = map_bookmarks_to_articles(articles)

  article_html = loader.render_to_string(
    'article.html',
    {'articles': articles, 'user': request.user, 'counter': 0, 'search': True},
    request=request
  )

  output_data = {
    'article_html': article_html
  }

  return JsonResponse(output_data)


def search_load_articles(request):
  output_data = {}
  request.session['index'] = request.session.get('index') + 10
  current_index = request.session.get('index')

  if current_index % 20 == 0:
    request.session['offset'] = request.session.get('offset') + 20

  current_offset = request.session.get('offset')
  search_query = ''

  if request.GET:
    search_query = request.GET['search']

  requestUrl = 'https://api.nytimes.com/svc/movies/v2/reviews/search.json?'\
    'offset='+str(current_offset)+'&query='+search_query+'&api-key='+API_KEY
  requestHeaders = {
    "Accept": "application/json"
  }

  response = requests.get(requestUrl, headers=requestHeaders)
  content = json.loads(response.content)
  articles = content['results'][(current_index%20):(current_index+10)%21]

  if request.user.is_authenticated:
    articles = map_bookmarks_to_articles(articles)

  article_html = loader.render_to_string(
    'article.html',
    {'articles': articles, 'user': request.user,
    'counter': current_index, 'search': True},
    request=request
  )

  output_data = {
    'article_html': article_html
  }

  return JsonResponse(output_data)

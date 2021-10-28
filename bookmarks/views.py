from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_protect

from .models import Bookmark, Folder

# Create your views here.
# def add_bookmark(request):

#     if not request.user.is_authenticated:
#         return redirect('index')

#     if request.method == 'POST':

def bookmarks_view(request):

    if not request.user.is_authenticated:
        return redirect('index')

    queries = Folder.objects.filter(user=request.user).order_by('name')
    folders = []

    for query in queries:
        query.bookmarks = Bookmark.objects.filter(
            user=request.user, folder=query)

        if query.bookmarks.exists():
            folders.append(query)

    return render(
    request, 'list.html', {'folders': folders})

@csrf_protect
def create_bookmark(request):
    if not request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        folder_id = request.POST.get('folder_id')
        link = request.POST.get('link')
        suggested_text = request.POST.get('suggestedText')
        byline = request.POST.get('byline')

        folder = Folder.objects.get(id=folder_id)

        bookmark = Bookmark.objects.create(
            folder=folder, user=request.user, link=link,
            link_text=suggested_text, byline=byline)
        data = serializers.serialize('json', [bookmark,])


        return JsonResponse({'success':True, 'bookmark': data})

    return JsonResponse({'success': False, 'errorMsg': 'Something went wrong.'})

def delete_bookmark(request):
    if not request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        bookmark_id = request.POST.get('bookmarkId')
        bookmark = Bookmark.objects.get(id=bookmark_id)
        bookmark.delete()

        return JsonResponse({'success':True})

    return JsonResponse({'success': False, 'errorMsg': 'Something went wrong.'})


def get_folders(request):
    if not request.user.is_authenticated:
        return redirect('index')

    query = Folder.objects.filter(user=request.user)
    query_json = serializers.serialize('json', query)

    return HttpResponse(query_json, content_type='application/json')


def create_folder(request):
    if not request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        folder_name = request.POST['name'].strip()
        folder = Folder.objects.create(name=folder_name, user=request.user)

        return JsonResponse({'success':True})

    return JsonResponse({'success': False, 'errorMsg': 'Something went wrong.'})
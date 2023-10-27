from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetModelSerializer
from rest_framework import status

@csrf_exempt
def list_create_snippet(request):
    # list all code snippets or create
    if request.method == 'GET':
        snippet = Snippet.objects.all()
        serializer = SnippetModelSerializer(snippet, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    
def retrieve_update_detsroy_snippet(request, pk):
    # retreive,update and delete snippet
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return status.HTTP_404_NOT_FOUND
    if request.method == 'GET':
        serializer = SnippetModelSerializer(snippet)
        return JsonResponse(serializer.data, status=200)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetModelSerializer(snippet, instance=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)



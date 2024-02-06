from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
# @api_view(['GET','POST'])
# def books(request):
#     return Response('list of the books', status=status.HTTP_200_OK)

# class BookList(APIView):
#     def get(self, request):
#         author = request.GET.get('author')
#         if(author):
#             return Response({'message':'list of the books by ' + author }, status.HTTP_200_OK)
        
#         return Response({'message':'list of the books'}, status.HTTP_200_OK)
    
#     def post(self, request):
#         return Response({'title':request.data.get('title')}, status.HTTP_201_CREATED)
    
# class Book(APIView):
#     def get(self, request, pk):
#         return Response({'message':'single book with id ' + str(pk)}, status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         return Response({'title':request.data.get('title')}, status.HTTP_200_OK)

@api_view(["GET", "POST"])
def menu_items(request):
    if request.method == 'GET':
        items= MenuItem.objects.select_related('category').all()
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)

@api_view(["GET", "POST"])
def single_item(request, id):
    item= get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)
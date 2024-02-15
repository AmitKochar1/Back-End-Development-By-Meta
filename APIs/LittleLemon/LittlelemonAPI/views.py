from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import status
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle

# Create your views here.
# class MenuItemView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
    
# class SingleMenuItemView(generics.RetrieveAPIView, generics.DestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer

@api_view(["POST", "GET"])
def menu_items(request):
    if(request.method =='GET'):
        items = MenuItem.objects.select_related("category").all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default =1)
        if category_name:
            items = items.filter(category__title = category_name)
        # double underscore __ allows you to access the model datafields through their category name.
        if to_price:
            items = items.filter(price = to_price) 
        # __lte means less then or equal to == and no lte means equal.
        if search:
            items = items.filter(title__contains = search)
        # __contain allows you to select an item with input from users
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)
            
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number = page)
        except EmptyPage:
            items = []
        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    elif request.method== "POST":
        serialized_item = MenuItemSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.validated_data, status.HTTP_201_CREATED)
    
    
@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

@api_view()
def secret_message():
    return "Some sceret message!!"

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='manager').exists():
        return Response({'message': 'only a manager should see this!!'})
    else:
        return Response({'message': "you are not authorized"}, 403)
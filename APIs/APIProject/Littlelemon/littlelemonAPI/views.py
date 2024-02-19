from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, throttle_classes, permission_classes
from rest_framework import status
from .models import Menuitem
from .serializers import MenuItemSerializer
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


# Create your views here.
@api_view(["POST", "GET"])
def menu_items(request):
    if(request.method == "GET"):
        items = Menuitem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        # pagination
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title = category_name)
        # category__title allows to map it model category. 
        if to_price:
            items = items.filter(price = to_price)
        # __lte - less then or equal or price to get exact price
        if search:
            items = items.filter(items__contains = search)
        # __contains allow to search for a particular item in items.
        if ordering:
            items = items.order_by(ordering)
            
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number = page)
        except EmptyPage:
            items = []
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)
    elif request.method == 'POST':
        serialized_items = MenuItemSerializer(data=request.data)
        serialized_items.is_valid(raise_exception=True)
        serialized_items.save()
        return Response(serialized_items.validated.data, status.HTTP_201_CREATED)
    
@api_view()
def single_item(request):
    item = get_object_or_404(Menuitem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({'message':'some secret message'})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='manager').exists():
        return Response({'message':'This is a manager view'})
    else:
        return Response({'message':'You are not authorised'}, 403)
    
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({'message':'successful'})

@api_view()
@throttle_classes([UserRateThrottle])
@permission_classes([IsAuthenticated])
def throttle_check_auth(request):
    return Response({'message':'This is for auth urser only'})
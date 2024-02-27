from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from .models import Menuitem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, ManagerListSerializer, CartHelpSerializer, CartSerializer, CartAddSerializer, CartRemoveSerializer, UserSerializer, OrderSerializer, SingleOrderSerializer, SingleHelperSerializer, OrderPutSerializer
from .paginations import MenuItemListPagination
from .permission import IsDeliveryCrew, IsManager
from django.contrib.auth.models import User, Group
import math
from datetime import date

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, throttle_classes, permission_classes
from rest_framework import status
from rest_framework import generics

class MenuItemListView(generics.ListCreateAPIView):
    throttle = [AnonRateThrottle, UserRateThrottle]
    queryset = Menuitem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ['title', 'category__title']
    ordering_fields = ['price', 'category']
    pagination_class = MenuItemListPagination
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
class CategoryView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    
    
class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Menuitem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        if self.request.method =='DELETE':
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def patch(self, request, *args, **kwargs):
        menuitem = Menuitem.objects.get(pk=self.kwargs['pk'])
        menuitem.featured = not menuitem.featured
        menuitem.save()
        return JsonResponse(status=200, data={'message':'Featured status of {} changed to {}'.format(str(menuitem.title), str(menuitem.featured))})

class ManagersListView(generics.ListCreateAPIView):
    throttle_classes= [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.all()
    serializer_class = ManagerListSerializer
    permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
    
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username = username)
            managers = Group.objects.get(name='Managers')
            managers.user_set.add(user)
            return JsonResponse(status=201, data={'message':'User added to Managers group'}) 
        
class ManagersRemoveView(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ManagerListSerializer
    permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
    queryset = User.objects.filter(group__name='manager')
    
    def delete()
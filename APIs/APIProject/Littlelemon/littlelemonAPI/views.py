from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from .models import Menuitem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, ManagerSerializer, CartHelpSerializer, CartSerializer, CartAddSerializer, CartRemoveSerializer, UserSerializer, OrderSerializer, SingleOrderSerializer, SingleHelperSerializer, OrderPutSerializer
from .paginations import MenuItemListPagination
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
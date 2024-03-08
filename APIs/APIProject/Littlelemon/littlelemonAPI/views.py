from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, ManagerListMenuItemSerializer, CartHelpSerializer, CartSerializer, CartAddSerializer, CartRemoveSerializer, UserSerializer, OrderSerializer, SingleOrderSerializer, SingleHelperSerializer, OrderPutSerializer
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
    queryset = MenuItem.objects.all()
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
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        if self.request.method =='DELETE':
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def patch(self, request, *args, **kwargs):
        menuitem = MenuItem.objects.get(pk=self.kwargs['pk'])
        menuitem.featured = not menuitem.featured
        menuitem.save()
        return JsonResponse(status=200, data={'message':'Featured status of {} changed to {}'.format(str(menuitem.title), str(menuitem.featured))})

class ManagersListView(generics.ListCreateAPIView):
    throttle_classes= [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.all()
    serializer_class = ManagerListMenuItemSerializer
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
    serializer_class = ManagerListMenuItemSerializer
    permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
    queryset = User.objects.filter(groups__name='Managers')
    
    def delete(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk =pk)
        managers = Group.objects.get(name='Managers')
        managers.user_set.remove(user)
        return JsonResponse(status=200, date={'message':'User removed from Manager group'})

class DeliveryCrewListView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name='Delivery crew')
    serializer_class=ManagerListMenuItemSerializer
    permission_classes = [IsAuthenticated, IsManager| IsAdminUser]
    
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            crew = Group.objects.get(name='Delivery crew')
            crew.user_set.add(user)
            return JsonResponse(status=201, data={'message':'User added to delivery Crew Group'})
        
        
class DeliveryCrewRemoveView(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ManagerListMenuItemSerializer
    permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
    queryset = User.objects.filter(groups__name = 'Delivery crew')
    
    def delete(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        user= get_object_or_404(User, pk=pk)
        managers = Group.objects.get(name='Delivery crew')
        managers.user_set.remove(user)
        return JsonResponse(status=201, data={'message':'User is removed'})
    
class CartOpertaionsView(generics.ListCreateAPIView):
    throttle_classes=[AnonRateThrottle, UserRateThrottle]
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self, *args, **kwargs):
        cart = Cart.objects.filter(user=self.request.user)
        return cart
    
    def post(self, request, *args, **kwargs):
        serialized_item = CartAddSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        id=request.data['menuitem']
        quantity = request.data['quantity']
        item = get_object_or_404(MenuItem, id=id)
        price= int(quantity) * item.price
        try:
            Cart.objects.create(user=request.user, quantity=quantity)
        except:
            return JsonResponse(status=409, data={'message':'item alredy exist in cart'})
        return JsonResponse(status=201, data={'message': 'Item added to Cart'}) 
    
    def delete(self, request, *args, **kwargs):
        if request.data['menuitem']:
            serialized_item= CartRemoveSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            menuitem = request.data['menuitem']
            cart = get_object_or_404(Cart, user= request.user, menuitem=menuitem)
            cart.delete()
            return JsonResponse(status=200, date={'message':'item removed from cart'})
        else:
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse(status=201, data={'message':'All items removed from cart'})

class OrderOperationsView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = OrderSerializer
        
    def get_queryset(self, *args, **kwargs):
        if self.request.user.groups.filter(name='Managers').exists() or self.request.user.is_superuser == True :
            query = Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery crew').exists():
            query = Order.objects.filter(delivery_crew=self.request.user)
        else:
            query = Order.objects.filter(user=self.request.user)
        return query

    def get_permissions(self):
        
        if self.request.method == 'GET' or 'POST' : 
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        return[permission() for permission in permission_classes]

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user)
        x=cart.values_list()
        if len(x) == 0:
            return HttpResponseBadRequest()
        total = math.fsum([float(x[-1]) for x in x])
        order = Order.objects.create(user=request.user, status=False, total=total, date=date.today())
        for i in cart.values():
            menuitem = get_object_or_404(MenuItem, id=i['menuitem_id'])
            orderitem = OrderItem.objects.create(order=order, menuitem=menuitem, quantity=i['quantity'])
            orderitem.save()
        cart.delete()
        return JsonResponse(status=201, data={'message':'Your order has been placed! Your order number is {}'.format(str(order.id))})

class SingleOrderView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = SingleOrderSerializer
    
    def get_permissions(self):
        order = Order.objects.get(pk=self.kwargs['pk'])
        if self.request.user == order.user and self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated, IsDeliveryCrew | IsManager | IsAdminUser]
        return[permission() for permission in permission_classes] 

    def get_queryset(self, *args, **kwargs):
            query = OrderItem.objects.filter(order_id=self.kwargs['pk'])
            return query


    def patch(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order.status = not order.status
        order.save()
        return JsonResponse(status=200, data={'message':'Status of order #'+ str(order.id)+' changed to '+str(order.status)})

    def put(self, request, *args, **kwargs):
        serialized_item = OrderPutSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        order_pk = self.kwargs['pk']
        crew_pk = request.data['delivery_crew'] 
        order = get_object_or_404(Order, pk=order_pk)
        crew = get_object_or_404(User, pk=crew_pk)
        order.delivery_crew = crew
        order.save()
        return JsonResponse(status=201, data={'message':str(crew.username)+' was assigned to order #'+str(order.id)})

    def delete(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order_number = str(order.id)
        order.delete()
        return JsonResponse(status=200, data={'message':'Order #{} was deleted'.format(order_number)})
    
    
# As per Meta
# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from .models import Category, MenuItem, Cart, Order, OrderItem
# from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, UserSerilializer
# from rest_framework.response import Response

# from rest_framework.permissions import IsAdminUser
# from django.shortcuts import  get_object_or_404

# from django.contrib.auth.models import Group, User

# from rest_framework import viewsets
# from rest_framework import status


# class CategoriesView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

#     def get_permissions(self):
#         permission_classes = []
#         if self.request.method != 'GET':
#             permission_classes = [IsAuthenticated]

#         return [permission() for permission in permission_classes]

# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
#     search_fields = ['category__title']
#     ordering_fields = ['price', 'inventory']

#     def get_permissions(self):
#         permission_classes = []
#         if self.request.method != 'GET':
#             permission_classes = [IsAuthenticated]

#         return [permission() for permission in permission_classes]


# class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer

#     def get_permissions(self):
#         permission_classes = []
#         if self.request.method != 'GET':
#             permission_classes = [IsAuthenticated]

#         return [permission() for permission in permission_classes]

# class CartView(generics.ListCreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Cart.objects.all().filter(user=self.request.user)

#     def delete(self, request, *args, **kwargs):
#         Cart.objects.all().filter(user=self.request.user).delete()
#         return Response("ok")


# class OrderView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             return Order.objects.all()
#         elif self.request.user.groups.count()==0: #normal customer - no group
#             return Order.objects.all().filter(user=self.request.user)
#         elif self.request.user.groups.filter(name='Delivery Crew').exists(): #delivery crew
#             return Order.objects.all().filter(delivery_crew=self.request.user)  #only show oreders assigned to him
#         else: #delivery crew or manager
#             return Order.objects.all()
#         # else:
#         #     return Order.objects.all()

#     def create(self, request, *args, **kwargs):
#         menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
#         if menuitem_count == 0:
#             return Response({"message:": "no item in cart"})

#         data = request.data.copy()
#         total = self.get_total_price(self.request.user)
#         data['total'] = total
#         data['user'] = self.request.user.id
#         order_serializer = OrderSerializer(data=data)
#         if (order_serializer.is_valid()):
#             order = order_serializer.save()

#             items = Cart.objects.all().filter(user=self.request.user).all()

#             for item in items.values():
#                 orderitem = OrderItem(
#                     order=order,
#                     menuitem_id=item['menuitem_id'],
#                     price=item['price'],
#                     quantity=item['quantity'],
#                 )
#                 orderitem.save()

#             Cart.objects.all().filter(user=self.request.user).delete() #Delete cart items

#             result = order_serializer.data.copy()
#             result['total'] = total
#             return Response(order_serializer.data)
    
#     def get_total_price(self, user):
#         total = 0
#         items = Cart.objects.all().filter(user=user).all()
#         for item in items.values():
#             total += item['price']
#         return total


# class SingleOrderView(generics.RetrieveUpdateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def update(self, request, *args, **kwargs):
#         if self.request.user.groups.count()==0: # Normal user, not belonging to any group = Customer
#             return Response('Not Ok')
#         else: #everyone else - Super Admin, Manager and Delivery Crew
#             return super().update(request, *args, **kwargs)



# class GroupViewSet(viewsets.ViewSet):
#     permission_classes = [IsAdminUser]
#     def list(self, request):
#         users = User.objects.all().filter(groups__name='Manager')
#         items = UserSerilializer(users, many=True)
#         return Response(items.data)

#     def create(self, request):
#         user = get_object_or_404(User, username=request.data['username'])
#         managers = Group.objects.get(name="Manager")
#         managers.user_set.add(user)
#         return Response({"message": "user added to the manager group"}, 200)

#     def destroy(self, request):
#         user = get_object_or_404(User, username=request.data['username'])
#         managers = Group.objects.get(name="Manager")
#         managers.user_set.remove(user)
#         return Response({"message": "user removed from the manager group"}, 200)

# class DeliveryCrewViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     def list(self, request):
#         users = User.objects.all().filter(groups__name='Delivery Crew')
#         items = UserSerilializer(users, many=True)
#         return Response(items.data)

#     def create(self, request):
#         #only for super admin and managers
#         if self.request.user.is_superuser == False:
#             if self.request.user.groups.filter(name='Manager').exists() == False:
#                 return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        
#         user = get_object_or_404(User, username=request.data['username'])
#         dc = Group.objects.get(name="Delivery Crew")
#         dc.user_set.add(user)
#         return Response({"message": "user added to the delivery crew group"}, 200)

#     def destroy(self, request):
#         #only for super admin and managers
#         if self.request.user.is_superuser == False:
#             if self.request.user.groups.filter(name='Manager').exists() == False:
#                 return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
#         user = get_object_or_404(User, username=request.data['username'])
#         dc = Group.objects.get(name="Delivery Crew")
#         dc.user_set.remove(user)
#         return Response({"message": "user removed from the delivery crew group"}, 200)
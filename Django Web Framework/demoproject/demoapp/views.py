from django.shortcuts import render
from django.http import HttpResponse
from .models import Menu

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def menu(request):
    return render(request, 'menu.html')


# def menu(request):
#     newmenu = {'pricechart':[
#         {'name': 'falafel', 'price':'12'},
#         {'name': 'Shawarma', 'price': '15'},
#         {'name': 'gyro', 'price': '20'},
#         {'name': 'humus', 'price': '15'},

#     ]}
#     return render(request,'menu.html', newmenu)

# retrieving data from databases
# def menu_by_id(request):
#     newmenu = Menu.objects.all()
#     newmenu_dict = {'menu': newmenu}
#     return render(request, 'menu_card.html', newmenu_dict)

# def about(request):
#     about_content={"about" : 'Based in chicago, illnois.'}
#     return render(request, 'about.html', about_content) 

# Create your views here.
# from demoapp.forms import LogForm

# def form_view(request):
#     form = LogForm()
#     if request.method == "POST":
#         form = LogForm(request.POST)
#         if form.is_valid():
#             form.save()
#     context = {'form': form}
#     return render(request, 'home.html', context) 


# def menuitems(request, dish):
#     items = {
#         "pasta": "Pasta is a type of noodle made from combination of wheat and grain",
#         "falafel": "Falafel are deep fried patties",
#         "cheesecake": "Cheesecake is a type of dessert",
#     }

#     description = items[dish]

#     return HttpResponse(f'<html><h1>{dish}</h1></html>' + description)

# def home(request):
#     path = request.path
#     scheme= request.scheme
#     method = request.method
#     address = request.META["REMOTE_ADDR"]
#     user_agent = request.META['HTTP_USER_AGENT']
#     path_info = request.path_info

#     response = HttpResponse()
#     response.headers['age'] = '20'

#     msg = f"""<br>
#         <br>Path:{path}
#         <br>Address: {address}
#         <br>Scheme: {scheme}
#         <br>Method: {method}
#         <br>User agent: {user_agent}
#         <br>Path info: {path_info}
#         <br>Response Header: {response.headers}
#     """
#     return HttpResponse(msg, content_type='text/html', charset='utf-8')
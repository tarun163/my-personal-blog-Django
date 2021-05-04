from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home(request):
    return render(request,'index.html')

def register(request):
    form = CreateUserForm()
   
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form':form}
    return render(request,'register.html',context)    

def login(request):
   if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        context = {'form':form }
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            user = authenticate(username = username, password = password)
            print(user)
            if user is not None:
                login(request, user)
                #return render(request,'index.html', {"name":username})
                return redirect('home' ) 
        else:
            return render(request, 'login.html',context)    

def search(request):
    context = {}
    return render(request,'search.html',context)            

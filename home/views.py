from django.shortcuts import render,HttpResponse

# Create your views here.

def home(request):
    return render(request,'index.html')

def register(request):
    context = {}
    return render(request,'register.html',context)    

def login(request):
    context = {}
    return render(request,'login.html',context) 

def search(request):
    context = {}
    return render(request,'search.html',context)            

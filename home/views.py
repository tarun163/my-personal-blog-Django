from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import CreateUserForm
from django.views import generic
from .models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def createblog(request):
    context = {'success':False}
    if request.method == 'POST':
        alltasks = Post.objects.all() 
        user = request.POST['user']
        title = request.POST['title']
        content = request.POST['content']
        status = request.POST['status']

        ins = Post(title=title,author=user,content=content,status=status)
        ins.save()
        context = {'success':True}
    return render(request,'createblog.html', context)

def search(request):
    return render(request,'search.html')   

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
    context = {}

    return render(request,'login.html',context) 
       
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3

class PostDetails(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'    
       
 
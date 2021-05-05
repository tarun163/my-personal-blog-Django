from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import CreateUserForm
from django.views import generic
from .models import Post
from django.contrib.auth import authenticate, login, logout
# Create your views here.


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

class PostDetails(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'    
       
def createblog(request):
    context = {}
    return render(request,'createblog.html', context)
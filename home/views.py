from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import CreateUserForm
from .forms import CommentForm
from django.views import generic
from .models import Post
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

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
    context = {'success':False}
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username,password)
            user = authenticate(username = username, password = password)
            print(user)
            if user is not None:
                loginUser(request, user)
                return redirect('home')

        else:
            return redirect('login')        


    return render(request,'login.html',context) 
       
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3

class PostDetails(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'  

def post_detail(request,slug):
    template_name = 'post_detail.html'  
    post = get_object_or_404(Post,slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)  
            new_comment.post = post
            new_comment.save() 

    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post':post,'comments':comments,'new_comment':new_comment,'comment_form':comment_form})

 
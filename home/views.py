from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import CreateUserForm
from .forms import CommentForm
from django.contrib import messages
from django.views import generic
from .models import Post,Profile
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import context
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import uuid
from django.http import HttpResponse
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
   
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
          
            try:
                if User.objects.filter(email = email).first():
                    messages.success(request,f'email is taken You are not able to log in')
                    return redirect('register')

                user_obj = User(username=username,email=email)
                user_obj.set_password(password)
                user_obj.save()
                auth_token = str(uuid.uuid4())
                print(auth_token)
                profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token)
                profile_obj.save()
                #form.save()
                send_mail_after_register(email,auth_token)
                return redirect('token_send')
            except Exception as e:
                print(e)        
            #mail part
           

    else:
        form = CreateUserForm()
    return render(request,'register.html',{'form':form,'title':'register here'})           

def send_mail_after_register(email,token):
    print("get")
    subject = 'your account need to verifide'
    message = f'hi press the link to varify account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list) 

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_varified:
                messages.success(request, 'your account is already verified')
                return redirect('home')

            profile_obj.is_varified = True
            profile_obj.save()
            messages.success(request, 'your account has verified')
            return redirect('success')
        else:
            return redirect('error')
    except Exception as e:
        print(e)  
        return redirect('error')
  

def success(request):
    return render(request,'success.html')

def error_page(request):
    return render(request,'error.html')

def token_send(request):
    return render(request,'token_send.html')       

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


def forget_password(request):
    print("get it")
    print( request.method )
    if request.method == 'POST':
        print("yes")
        email = request.POST.get('email')
        print(email)
        user = User.objects.filter(email = email).first()
        print(user)
        if user is not None:
            profile_obj = Profile.objects.filter(user = user).first()
            print(profile_obj.auth_token)
            auth_token = str(uuid.uuid4())
            profile_obj.auth_token = auth_token
            profile_obj.save()
            request.session['email']=email
            #Profile.auth_token = auth_token
            send_mail_for_reset(email,auth_token)
            return redirect('token_send')
        else:    
            messages.success(request, 'please enter valid email address') 
            return render(request,'forget_password.html')   
            

    return render(request,'forget_password.html')
  
def send_mail_for_reset(email,token):
    subject = 'your account need to verifide'
    message = f'hi press the link to varify account http://127.0.0.1:8000/reset_verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    send_mail(subject,message,email_from,recipient_list)   

def reset_verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        print(profile_obj.user)
        if profile_obj:           
            messages.success(request, 'your can reset your password here')
            return redirect('reset_password')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)  
        return redirect('/error')

def reset_password(request):  
    email=request.session['email']
    print(email)
    if request.method == 'POST':        
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            print(email ,password1,password2)
            password = make_password(password1)
            q = User.objects.filter(email = email).update(password = password)
            return redirect('login')
    return render(request,'reset_password.html') 
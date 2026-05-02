from django.shortcuts import render,redirect
from .forms import UserForm,UserpData,Updateform,UpdateprofileForm,ResetPasswordForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import User
from defects.models import Developers,Defects_details


# Create your views here.
def registeration(request):
    registered = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        form1 = UserpData(request.POST,request.FILES)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            profile = form1.save(commit=False)
            profile.user = user # both model is merged together
            profile.save()
            registered = True
    else:
        form = UserForm()
        form1 = UserpData()
    context={
        'form':form,
        'form1':form1,
        'registered':registered
    }
    
    return render(request,'accounts/registeration.html',context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password= request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('home')
            else:
                return HttpResponse("User is not active")
        else:
            return HttpResponse("Please check your details......")
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def home(request):
    defect = Defects_details.objects.all().count()
    pdefect = Defects_details.objects.filter(defect_status='not completed').count()
    cdefect = Defects_details.objects.filter(defect_status='completed').count()
    context = {
        'defect':defect,
        'pdefect':pdefect,
        'cdefect':cdefect
    }
    return render(request,'accounts/home.html',context)

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    developer = False
    total_defect=0
    pending_defect=0
    complete_defect=0
    try:
        dev = Developers.objects.get(dev_name=request.user) 
        total_defect = Defects_details.objects.filter(assigned_to=dev).count()
        pending_defect = Defects_details.objects.filter(assigned_to=dev, defect_status='not completed').count()
        complete_defect = Defects_details.objects.filter(assigned_to=dev, defect_status='completed').count()

        if dev:
            developer = True
    except Developers.DoesNotExist:
        dev = None
    context = {
        'developer':developer,
        'total_defect':total_defect,
        'pending_defect':pending_defect,
        'complete_defect':complete_defect
    }
    return render(request,'accounts/profile.html',context)

@login_required(login_url='login')
def update(request):
    if request.method == 'POST':
        form = Updateform(request.POST,instance=request.user)
        form1 = UpdateprofileForm(request.POST,request.FILES,instance=request.user.userdata)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.save()

            profile = form1.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('profile')

    else:
        form = Updateform(instance=request.user)
        form1 = UpdateprofileForm(instance=request.user.userdata)
    context={
        'form':form,
        'form1':form1
    }  
    return render(request,'accounts/update.html',context)

def reset_password(request):
    passw=False
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            passw=True
            #return redirect('')

    else:
        form = ResetPasswordForm()
    return render(request,'accounts/forgotpassword.html',{'form':form,'passw':passw})

def demo(request):
    d=User.objects.all()
    return render(request,'defects/demo.html',{'d':d})

from django.shortcuts import render,redirect
from defects.models import Defects_details,Testers,Defect_Screen_Shots,Developers
from django.contrib.auth.decorators import login_required
from defects.forms import defdetails,add_defectdetails
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from defects.utils import send_email_view

# Create your views here.
@login_required(login_url='login')
def defect_detail(request):
    data = Defects_details.objects.all()
    total_det = len(data)
    user=request.user
    show_button=False
    can_edit = False
    can_delete = False

    try:
        test = Testers.objects.get(tester_name=user)
        if test.is_admin:
            show_button=True
            can_edit = True
            can_delete = True
    except Testers.DoesNotExist:
        test = None
    paginator = Paginator(data,5)
    page_num = request.GET.get('pg')
    vaename = paginator.get_page(page_num)
    context = {
        'data': vaename,
        'td':total_det,
        'show_button':show_button,
        'can_edit': can_edit,
        'can_delete': can_delete,

    }

    return render(request, 'defects/alldefects.html',context )

@login_required(login_url='login')
def description(request,id=0):
    des = Defects_details.objects.get(id=id)
    dimg = Defect_Screen_Shots.objects.filter(defect=des)
    return render(request,'defects/description.html',{'des':des,'dimg':dimg})

@login_required(login_url='login')
def edit_defect(request,id=0):
    defect = Defects_details.objects.get(id=id)
    if request.method == 'POST':
        form = defdetails(request.POST,instance=defect)
        if form.is_valid():
            form.save()
            return redirect('defectdetal')
    else:
        form = defdetails(instance=defect)
    return render(request,'defects/edit.html',{'form':form})

@login_required(login_url='login')
def add_defects(request):
    if request.method == 'POST':
        form = add_defectdetails(request.POST)
        if form.is_valid():
            devname = form.cleaned_data['assigned_to']
            user= User.objects.get(username=devname)
            form.save()
            send_email_view(user.email)
            return redirect('defectdetal')
    else:
        form = add_defectdetails()
    return render(request,'defects/adddefect.html',{'form':form})


def pending_defects(request):
    data = Defects_details.objects.filter(defect_status='not completed')
    total_det = len(data)
    user=request.user
    show_button=False
    can_edit = False
    can_delete = False

    try:
        test = Testers.objects.get(tester_name=user)
        if test.is_admin:
            show_button=True
            can_edit = True
            can_delete = True
    except Testers.DoesNotExist:
        test = None
    paginator = Paginator(data,4)
    page_num = request.GET.get('pg')
    vaename = paginator.get_page(page_num)
    context = {
        'data': vaename,
        'td':total_det,
        'show_button':show_button,
        'can_edit': can_edit,
        'can_delete': can_delete,

    }
    return render(request,'defects/pending.html',context)
def completed_defects(request):
    data = Defects_details.objects.filter(defect_status='completed')
    total_det = len(data)
    user=request.user
    show_button=False
    can_edit = False
    can_delete = False

    try:
        test = Testers.objects.get(tester_name=user)
        if test.is_admin:
            show_button=True
            can_edit = True
            can_delete = True
    except Testers.DoesNotExist:
        test = None
    paginator = Paginator(data,4)
    page_num = request.GET.get('pg')
    vaename = paginator.get_page(page_num)
    context = {
        'data': vaename,
        'td':total_det,
        'show_button':show_button,
        'can_edit': can_edit,
        'can_delete': can_delete,

    }
    return render(request,'defects/completed.html',context)


def filter_defect(request):
    dev=Developers.objects.all()
    data = Defects_details.objects.all()
    td = len(data)
    tadmin=False
    if request.method == 'POST':
        username = request.POST['username']
        if username:
            try:
                duser = User.objects.get(username=username)
                developer = Developers.objects.get(dev_name=duser)
                data = Defects_details.objects.filter(assigned_to=developer)
                td = len(data)
                try:
                    test = Testers.objects.get(tester_name=request.user)
                    if test.is_admin:
                        tadmin=True
                except Testers.DoesNotExist:
                    test = None
            except Developers.DoesNotExist as e:
                print(e)
                

    context = {
        'data': data,
        'td': td,
        'dev':dev,
        'tadmin':tadmin
    }
    return render(request, 'defects/filterdefects.html', context)

def delete_defect(request,id=0):
    defect = Defects_details.objects.get(id=id)
    if request.method == 'POST':
        if 'yes' in request.POST:
            defect.delete()
            return redirect('defectdetal')  
        else:
            return redirect('defectdetal') 


    return render(request,'defects/delete.html',{'defect':defect})
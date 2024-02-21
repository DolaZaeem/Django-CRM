from django.shortcuts import render , redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm , AddQtOvr
from .models import Quote_ovr

# Create your views here.

def home(request):
    records = Quote_ovr.objects.all()


    # Check to see if loginig in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have been logged in ")
            return redirect('home')
        else:
            messages.success(request,"There was an error logging in please try again...")
            return redirect('home')
    else:
        return render(request,'home.html',{'records':records})



def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out")
    return redirect('home')



def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and Login 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request, user)
            messages.success(request,"Welcome")
            return redirect('home')
    else:
        form =SignUpForm()
        return render(request,'register.html',{'form':form})
    return render(request,'register.html',{'form':form})


def customer_record(request,pk):
    if request.user.is_authenticated:
        #Look up record
        customer_record = Quote_ovr.objects.get(id=pk)
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.success(request,"Log in to view details of records")
        return redirect('home')
    
def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it = Quote_ovr.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Record Deleted Successfully")
        return redirect('home')
    else:
        messages.success(request,"You must be logged in to delete that")
        return redirect('home')
    
def add_record(request):
    if request.method == 'POST':
        form = AddQtOvr(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Added record")
            return redirect('home')
    else:
        form =AddQtOvr()
        return render(request,'add_record.html',{'form':form})
    return render(request,'add_record.html',{'form':form})


def update_record(request,pk):
    if request.user.is_authenticated:
        current_record = Quote_ovr.objects.get(id=pk)
        form = AddQtOvr(request.POST or None,instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record has been update")
            return redirect('home')
        return render(request,'update_record.html',{'form':form})
    else:
        messages.success(request,"You must be logged in.")
        return redirect('home')
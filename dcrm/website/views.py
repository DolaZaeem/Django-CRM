from django.shortcuts import render , redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm , AddQtOvr,AddQtDetail
from .models import Quote_ovr , Quote_det
from django.db.models import Q

# Create your views here.

def home(request):
    records = Quote_ovr.objects.filter(quote_det__isnull=False)
   
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
        quote_det = Quote_det.objects.filter(Quote_no=pk)
   
        return render(request,'record.html',{'customer_record':customer_record,"quote_details":quote_det})
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
            return redirect('add_items', pk=form.instance.pk)
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
    
def add_items(request, pk):
    if request.user.is_authenticated:
        quote_ovr = Quote_ovr.objects.get(id=pk)
        if request.method == 'POST':
            form = AddQtDetail(request.POST)
            if form.is_valid():
                form.instance.Quote_no = quote_ovr
                form.save()
                return redirect('record', pk=quote_ovr.pk)
        else:
            form = AddQtDetail()
        return render(request, 'add_items.html', {'form': form, 'quote_ovr': quote_ovr})
    else:
        return redirect('login')
    
def update_item(request,pk):
    if request.user.is_authenticated:
        current_record = Quote_det.objects.get(id=pk)
        form = AddQtDetail(request.POST or None,instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record has been update")
            return redirect('home')
        return render(request,'item_details.html',{'form':form})
    else:
        messages.success(request,"You must be logged in.")
        return redirect('home')
    
def delete_items(request,pk):
    if request.user.is_authenticated:
        delete_it = Quote_det.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Item Deleted Successfully")
        return redirect('home')
    else:
        messages.success(request,"You must be logged in to delete that")
        return redirect('home')
    
def Incomplete(request):
    if request.user.is_authenticated:
        records = Quote_ovr.objects.filter(quote_det__isnull=True)
        return render(request, 'Incomplete.html', {'records':records})
    else:
        messages.success(request,"You must be logged in to view that")
        return redirect('home')
    
def search(request):
    if request.user.is_authenticated:
        query = request.GET.get('q')
        if query:
            quote_det = Quote_det.objects.filter(Q(Item_name__icontains=query)|Q(Item_no__icontains=query)|Q(Item_qty__icontains=query))
            quote_ovr = Quote_ovr.objects.filter(Q(Customer_name__icontains=query)|
                                                Q(Quote_date__icontains=query)|
                                                Q(Quote_no__icontains=query)|
                                                Q(City__icontains=query)|
                                                Q(Address__icontains=query)|
                                                Q(State__icontains=query)|
                                                Q(Currency__icontains=query)|
                                                Q(Zipcode__icontains=query))
            context = {'query':query,'quote_det': quote_det, 'quote_ovr': quote_ovr}
            return render(request, 'search_results.html', context)
        else:
            return render(request, 'search_form.html')
    else:
        messages.success(request,"You must be logged in to view that")
        return redirect('home')
from django.forms import ValidationError
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm , AddQtOvr,AddQtDetail
from .models import Quote_ovr , Quote_det
from .resources import Quote_detResource,Quote_ovrResource
from tablib import Dataset
from django.db.models import Q
import openpyxl as xl
import pandas as pd

# Create your views here.

def home(request):
    records = Quote_ovr.objects.filter(quote_det__isnull=False).distinct()
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
            messages.success(request,"Record has been updated")
            return redirect('record', pk=current_record.Quote_no)
            
        return render(request,'item_details.html',{'form':form})
    else:
        messages.success(request,"You must be logged in.")
        return redirect('home')
    
def delete_items(request,pk):
    if request.user.is_authenticated:
        delete_it = Quote_det.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Item Deleted Successfully")
        return redirect('record', pk=delete_it.Quote_no)
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

def importdata(request):
  
    if request.user.is_authenticated:
        if request.method == 'POST':
            file = request.FILES['file']
            header_checked = bool(request.POST.get('h1'))
            header_index = None
            if header_checked:
                header_index = 0

            workbook = pd.read_excel(file,sheet_name=['Sheet1','Sheet2'],header=header_index)
            sheet1 = workbook['Sheet1'].values
            sheet2 = workbook['Sheet2'].values
            # process the data from the sheets here
            # Ignore the first row of sheet1 if h1 is checked
            
            for x in range(0,len(sheet1)):
                    try:
                        # Create a new instance of the Quote_ovr model
                        quote_ovr = Quote_ovr()
                        quote_ovr.Quote_no = sheet1[x,2]
                        quote_ovr.Quote_date = pd.to_datetime(sheet1[x,3],yearfirst=1)
                        quote_ovr.Customer_name = sheet1[x,4]
                        quote_ovr.Customer_email = sheet1[x,5]
                        quote_ovr.Phone = sheet1[x,6]
                        quote_ovr.Address = sheet1[x,7]
                        quote_ovr.City = sheet1[x,8]
                        quote_ovr.State = sheet1[x,9]
                        quote_ovr.Zipcode = sheet1[x,10]
                        #quote_ovr.Currency = sheet1[x,11]
                        if quote_ovr.Currency in ['EUR','USD','GBP']:
                            quote_ovr.Currency = sheet1[x,11]
                            print(sheet1[x,11])
                        else:
                             messages.error(request, f"Error: Invalid data in row {x} CURRENCY COLUMN. Please check the data and try again for Quote overviews")
                             break
                        quote_ovr.save()
                    except ValidationError as e:
                        messages.error(request, f"Error: Invalid data in row {x}{e}. Please check the data and try again.")
                        return render(request, 'importdata.html')
                    

            for x in range(0,len(sheet2)):
                try:
                  quotes_ovr_instance = Quote_ovr.objects.get(pk=sheet2[x,2])
                  quote_det = Quote_det.objects.create(Quote_no=quotes_ovr_instance,
                  Item_name = sheet2[x,3],
                  Item_qty = sheet2[x,4],
                  Item_no = sheet2[x,5],
                  Item_per_unit_price = sheet2[x,6])
                except ValidationError as e:
                    messages.error(request, f"Error: Invalid data in row {x}. Please check the data and try again.")
                    return render(request, 'importdata.html')
                except Quote_ovr.DoesNotExist:
                    messages.error(request, f"Error: Foreign key-primary key mismatch in row {x}. Please check the data and try again.")
                    return render(request,'importdata.html')

            messages.success(request,"Data imported")
        return render(request, 'importdata.html')
    else:
        return render(request, 'login.html')
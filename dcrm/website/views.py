from django.forms import ValidationError
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm , AddQtOvr,AddQtDetail , SuggestPriceForm
from .models import Quote_ovr , Quote_det
from django.db.models import Q
import pandas as pd
from django.core.exceptions import ValidationError
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime
import pickle
from sklearn.svm import SVR
import os
from django.shortcuts import render, get_object_or_404


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


def quote_record(request,quote_no_ref):
    if request.user.is_authenticated:
        #Look up record
        quote_record = Quote_ovr.objects.get(Quote_no=quote_no_ref)
        quote_det = Quote_det.objects.filter(Quote_ref=quote_no_ref)
   
        return render(request,'record.html',{'quote_record':quote_record,"quote_details":quote_det})
    else:
        messages.success(request,"Log in to view details of records")
        return redirect('home')
    
def delete_record(request,quote_no_ref):
    if request.user.is_authenticated:
        delete_it = Quote_ovr.objects.get(Quote_no=quote_no_ref)
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
            return redirect('add_items', quote_no_ref=form.instance.Quote_no)
    else:
        form =AddQtOvr()
        return render(request,'add_record.html',{'form':form})
    return render(request,'add_record.html',{'form':form})


def update_record(request,quote_no_ref):
    if request.user.is_authenticated:
        current_record = Quote_ovr.objects.get(Quote_no=quote_no_ref)
        form = AddQtOvr(request.POST or None,instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record has been update")
            return redirect('record',quote_no_ref=form.instance.Quote_no)
        return render(request,'update_record.html',{'form':form})
    else:
        messages.success(request,"You must be logged in.")
        return redirect('home')
    
def add_items(request, quote_no_ref):
    if request.user.is_authenticated:
        quote_ovr = Quote_ovr.objects.get(Quote_no=quote_no_ref)
        if request.method == 'POST':
            form = AddQtDetail(request.POST)
            if form.is_valid():
                form.instance.Quote_ref = quote_ovr
                form.save()
                messages.success(request,"Item has been added")
                return redirect('record', quote_no_ref=quote_ovr.Quote_no)
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
            return redirect('record', quote_no_ref=current_record.Quote_ref)
            
        return render(request,'item_details.html',{'form':form,'current_record':current_record})
    else:
        messages.success(request,"You must be logged in.")
        return redirect('home')
    
def delete_items(request,pk):
    if request.user.is_authenticated:
        delete_it = Quote_det.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Item Deleted Successfully")
        return redirect('record', quote_no_ref=delete_it.Quote_ref)
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
                                                Q(Country__icontains=query)|
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
                    quote_ovr_model = Quote_ovr()
                    quote_ovr_model.Quote_no = sheet1[x,2]
                    quote_ovr_model.Quote_date = pd.to_datetime(sheet1[x,3],yearfirst=1)
                    quote_ovr_model.Customer_name = sheet1[x,4]
                    quote_ovr_model.Customer_email = sheet1[x,5]
                    quote_ovr_model.Phone = sheet1[x,6]
                    quote_ovr_model.Country = sheet1[x,7]
                    quote_ovr_model.City = sheet1[x,8]
                    quote_ovr_model.State = sheet1[x,9]
                    quote_ovr_model.Zipcode = sheet1[x,10]
                    quote_ovr_model.Currency = sheet1[x,11]
                    quote_ovr_model.save()
                    
                except ValidationError as e:
                    # Handle integrity errors here
                    messages.error(request, f"Error: Invalid form entry error at row {x+1}.")
                except Exception as e:
                    # Handle other exceptions here
                    messages.error(request, f"Error: something went wrong at row{x+1}.{e}")

            for x in range(0,len(sheet2)):
                try:
                  quote_det_model = Quote_det()
                  instance = Quote_ovr.objects.get(Quote_no = sheet2[x,2])
                  quote_det_model.Quote_ref = instance
                  quote_det_model.Item_name = sheet2[x,3]
                  quote_det_model.Item_qty = sheet2[x,4]
                  quote_det_model.Item_no = sheet2[x,5]
                  quote_det_model.Item_per_unit_price = sheet2[x,6]
                  quote_det_model.save()
        
                except ValidationError as e:
                    messages.error(request, f"Error: Invalid data in row {x}. Please check the data and try again.")
                    return render(request, 'importdata.html')
                except Quote_ovr.DoesNotExist:
                    messages.error(request, f"Error: Foreign key-primary key mismatch in row {x}. Please check the data and try again.")
                    return render(request,'importdata.html')
                except TypeError as e:
                    messages.error(request,f"Error:{e} at  row {x} ")
        
            messages.success(request,"Data imported")
        return render(request, 'importdata.html')
    else:
        return render(request, 'login.html')
    


def train_svm(request):
    # Set the path to the pickle file
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    models_path = os.path.join(downloads_path, "Trained Models")
    pickle_path = os.path.join(models_path, 'training_details.pkl')
   

    # Check if the pickle file exists
    if os.path.isfile(pickle_path):
        # Load the training details from the pickle file
        with open(pickle_path, 'rb') as f:
            training_details = pickle.load(f)
    else:
        # Initialize the training details
        training_details = {
            "date_trained": None,
            "num_records": None,
            "mse": None
        }

    if 'train' in request.GET:
        # Perform the SVM training
        data = []
        queryset = Quote_ovr.objects.all()
        for quote_ovr in queryset:
            quote_det = Quote_det.objects.filter(Quote_ref=quote_ovr.Quote_no)
            for item in quote_det:
                data.append([
                    quote_ovr.Customer_Type,
                    quote_ovr.Country.lower(),
                    item.Item_name.lower(),
                    item.Item_per_unit_price,
                ])

        # Create a dataframe from the data
        df = pd.DataFrame(data, columns=['Customer_Type', 'Country', 'Item_name', 'Item_per_unit_price'])

        # Convert the 'Item_per_unit_price' column to numeric values
        df['Item_per_unit_price'] = pd.to_numeric(df['Item_per_unit_price'])

        # Select the desired columns for the feature data
        X_data = df[['Customer_Type', 'Country', 'Item_name']]

        # Prepare the OneHotEncoder and fit to the feature data
        encoder = OneHotEncoder()
        X_encoded = encoder.fit_transform(X_data)

        # Prepare the target data
        y_data = df['Item_per_unit_price']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_data, test_size=0.2, random_state=42)

        # Train the SVM model
        model = SVR(kernel='linear', C=1e3,epsilon=0.2)
        model.fit(X_train, y_train)

        # Calculate the MSE of the model
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)

        # Save the training details
        training_details = {
            "date_trained": datetime.now(),
            "num_records": len(data),
            "mse": round(mse,2)
        }

       # Save the model and the encoder
        models_path = os.path.join(os.path.expanduser("~"), "Downloads", "Trained Models")
        if not os.path.exists(models_path):
            os.makedirs(models_path)
        with open(os.path.join(models_path, 'model.pkl'), 'wb') as file:
            pickle.dump(model, file)
        with open(os.path.join(models_path, 'encoder.pkl'), 'wb') as file:
            pickle.dump(encoder, file)

        # Save the training details to the pickle file
        with open(pickle_path, 'wb') as f:
            pickle.dump(training_details, f)

  
        # Display success message
        messages.success(request, "Training successful!")
        print(X_encoded[0][0:52])
       

    return render(request, 'train_svm.html', {'training_details': training_details})

def suggest_price(request):
    if request.method == 'POST':
        form = SuggestPriceForm(request.POST)
        if form.is_valid():
            item_name = request.POST['item_name'].lower()
            country = request.POST['country'].lower()
            customer_type = request.POST['customer_type']  
            
            # Check if the model file exists
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            models_path = os.path.join(downloads_path, "Trained Models")
            pickle_path = os.path.join(models_path, 'model.pkl')
            if not os.path.isfile(pickle_path):
                messages.error(request, "The model file does not exist.")
                return render(request, 'suggest_price.html')

            # Load the model
            with open(pickle_path, 'rb') as f:
                model = pickle.load(f)

            # Prepare the input data for the model
            input_data = pd.DataFrame({'Item_name': [item_name],
                                        'Country': [country],
                                        'Customer_Type': [customer_type]},
                                    index=[0])

            # Prepare the OneHotEncoder and fit to the feature data
            # Fit the encoder using the training data
            with open(os.path.join(models_path, 'encoder.pkl'), 'rb') as f:
                encoder = pickle.load(f)
        
            X_new_encoded = encoder.transform(input_data[['Customer_Type', 'Country', 'Item_name']])

            # Reshape to a 2D array to fit the model's input shape
            X_new_encoded = X_new_encoded.toarray().reshape(1, -1)
    
            # Add the remaining features with a value of zero
        
            

            # Make the prediction
            suggestion = model.predict(X_new_encoded)
            return render(request, 'suggest_price.html', {'form': form, 'suggestion': round(suggestion[0],2)})
    else:
        form = SuggestPriceForm()
        return render(request, 'suggest_price.html', {'form': form})
    
 
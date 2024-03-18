from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Quote_ovr,Quote_det



class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))

    first_name = forms.CharField(label="",max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))

    last_name = forms.CharField(label="",max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

#Create A Quote overview Form
class AddQtOvr(forms.ModelForm):
    Quote_no  = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':"Quote No.","class":"form-control","autocomplete":"off"}),label="")
    Quote_date = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={'placeholder':"Quote Date","class":"form-control","type":"date"}),label="")
    Customer_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':"Customer Name","class":"form-control"}),label="")
    Customer_email = forms.CharField(required=True, widget=forms.widgets.EmailInput(attrs={'placeholder':"Customer Email","class":"form-control"}),label="")
    Phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':"Phone","class":"form-control"}),label="")
    Country = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':"Country","class":"form-control"}),label="")
    City = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':"City","class":"form-control"}),label="")
    State =forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':"State","class":"form-control"}),label="")
    Zipcode = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':"Zipcode","class":"form-control"}),label="")
    Currency = forms.ChoiceField(required=True, choices=Quote_ovr.CURRENCY, widget=forms.widgets.Select(attrs={'class':'form-control'}),label="")
    Customer_Type = forms.ChoiceField(required=True, choices=Quote_ovr.CustomerType, widget=forms.widgets.Select(attrs={'class':'form-control'}),label="")
    class Meta:
            model = Quote_ovr
            fields = ['Quote_no', 'Quote_date', 'Customer_name', 'Customer_email', 'Phone', 'Country', 'City', 'State', 'Zipcode','Currency',"Customer_Type"]
            exclude = ('user',)
#Create A Quote Detail Form
class AddQtDetail(forms.ModelForm):
    '''Quote_no  = forms.ModelChoiceField(queryset=Quote_ovr.objects.all(), widget=forms.widgets.Select(attrs={'placeholder':"Quote No.","class":"form-control"}),label="")'''
    Item_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':"Item Name","class":"form-control"}),label="")
    Item_qty = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={'placeholder':"Item Qty","class":"form-control"}),label="")
    Item_no = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':"Item no","class":"form-control"}),label="")
    Item_per_unit_price = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={'placeholder':"Per unit Price","class":"form-control"}),label="")



    class Meta:
        model = Quote_det
        fields = ['Item_name','Item_qty','Item_no','Item_per_unit_price']
        exclude =("user","Quote_ref","product_line_total")    


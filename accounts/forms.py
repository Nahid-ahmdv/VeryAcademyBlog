from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm #we're essentially just gonna extend some of the existing code that exists in django 'AuthenticationForm' class\form. we just want to extend the form or overwrite the existing form so that l can include our own CSS styling of our form.(AuthenticationForm is referring to the login form)
# https://docs.djangoproject.com/en/3.0/topics/auth/default/
# https://docs.djangoproject.com/en/3.0/topics/forms/
#دو تا کامنت بالا لینک‌هایی هستن برای مطالعه بیشتر در داکیومنتیشن خود جنگو
from django.contrib.auth.models import User #برای فرم مربوط به ولیدیشن است  #we're gonna need to utilize the (built-in) "User" table for our registration form
from django.core.exceptions import ValidationError

class UserLoginForm(AuthenticationForm): #a custom authentication form that inherits from 'AuthenticationForm' #l'm gonna define what l want in this form. so obviously what l want in this form is the username and password. so let's just go ahead and create that, but we're gonna update the form to include the class and the other parameters, attributes we want to include. so we can style our form.
    #توضیحات مربوط به علت پیاده‌سازی این روش در نوت گوشی
    '''custom fields'''
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'})) #mb=margin bottom
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))
   #these two fields, 'username' and 'password', are self-explanatory obviously l need to make sure that the fields that are in the existing form actually exist here otherwise this simply would be no point. so the login form just has a username and password.
   #همون‌طور که در نت گوشیم توضیح دادم this is just another way of adding attributes 

###The code snippet below is part of a Django form class that uses the 'ModelForm' functionality to create a form based on a model, specifically for user registration.
#registration form: (note that all these form inputs are just mirroring what is already existing) در واقع ما اگه خودمون هم می‌خواستیم یک فرمی بسازیم این فیلدها رو حتما می‌داشت
class RegistrationForm(forms.ModelForm): #that is extending from the ModelForm.
    '''custom fields'''
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput) #for entering their original password.
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)  #for confirming (repeating) their original password.
    '''
    widget=forms.PasswordInput: ورودی را نقطه نقطه نمایش می‌دهد
    This indicates that the input field should use the 'PasswordInput' widget.
    Purpose: The 'PasswordInput' widget renders an HTML <input> element of type password, which masks the characters entered by the user (e.g., displaying dots or asterisks instead of plain text). This is a common practice for security reasons when entering sensitive information like passwords.
    '''

    #The Meta class is an inner class used to provide metadata to the 'ModelForm'. It allows you to configure how the form behaves and which model it is associated with.
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',)#This tuple specifies which fields from the User model should be included in the form.
    
    #we're gonna check to make sure that usernames are unique in our system.
    def clean_username(self): #برای چک کردن اینکه  یه وقت یوزرنیم تکراری نباشه، البته شاید شما بخواهید که به جای یوزرنیم ایمیل یونیک باشد 
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username
    
    def clean_password2(self): #برای اینکه مطمئن بشیم پسورد و تکرار پسورد یکسان بوده
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self): #برای اینکه مطمئن بشیم ایمیلی که یوزر وارد کرده هم یونیک و غیرتکراری است
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists(): #we're checking to see if email (that user entered) equals email within the system (database).
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email
    def __init__(self, *args, **kwargs): #we add some classes to the 'username', 'email',and... so we can get these fields to look how we want.
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self): #we're gonna check to see if the email the user has typed in exists in our database
        email = self.cleaned_data['email']
        test = User.objects.filter(email=email)
        if not test:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class PwdResetConfirmForm(SetPasswordForm):  #There is two inputs for this form.
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class UserEditForm(forms.ModelForm): #we're just building a custom form here extending from "ModelForm".

    first_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))

    last_name = forms.CharField(
        label='Lastname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Lastname', 'id': 'form-lastname'}))

    email = forms.EmailField(
        max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-email'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self): #احیانا اگر یوزرمان خواست ایمیلش را اپدیت کند پس از وارد کردن ایمیل جدید به کمک این متد چکش می‌کنیم تا ببینیم وجود دارد از قبل در دیتابیس‌مون یا خیر
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_name'].required = False
        self.fields['email'].required = False

class PwdChangeForm(PasswordChangeForm): #The user's gonna need to type in their old password and then new password twice.

    old_password = forms.CharField(
        label='Old Password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-oldpass'}))
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))
'''
In Django, the relationship between the fields defined in a form (like 'username', 'email', 'password', and 'password2') and the fields specified in the Meta class (like those associated with the 'User' model) is established through the use of a 'ModelForm'. Here’s how this relationship works:
1. ModelForm Basics
When you create a form by inheriting from 'forms.ModelForm', Django automatically connects the form fields to the fields of the specified model. This allows you to define custom fields in your form while still linking them to the model's structure.
2. Field Mapping
Custom Fields: In your form, you can define custom fields like 'username', 'email', 'password', and 'password2'. These fields are not automatically tied to the model unless specified in the Meta class.
Meta Class: The Meta class specifies which model to use (model = User) and which fields from that model should be included in the form (fields = ('username', 'email', 'first_name',)).
3. Field Relationship
Matching Names: The fields defined in your form (like 'username' and 'email') should match the names of the corresponding fields in the model. Django uses these names to understand how to map data between the form and the model.
Validation and Saving: When you call form.is_valid() and then save the form, Django will:
Validate that the data entered into these fields complies with any constraints defined in both the form and the model.
If valid, it will create an instance of the model (in this case, a User object) using data from those fields.
Example of How It Works
Here’s a step-by-step explanation of how Django handles this relationship:
Form Definition:
You define a form with custom fields:
python
username = forms.CharField(label='Enter Username', min_length=4, max_length=50, help_text='Required')
email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'Sorry, you will need an email'})
password = forms.CharField(label='Password', widget=forms.PasswordInput)
password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

Meta Class:
You specify that this form is based on the User model and include relevant fields:
python
class Meta:
    model = User
    fields = ('username', 'email', 'first_name',)

Form Submission:
When a user submits this form, you typically handle it in a view:
python
if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
        # Create a new User instance
        user = User(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name']
        )
        user.set_password(form.cleaned_data['password'])  # Hashing password
        user.save()  # Save user to database

Data Handling:
The data entered into 'username', 'email', and other fields is accessed via 'form.cleaned_data'.
The custom field for password (password) is not directly tied to any field in the User model unless you explicitly handle it (e.g., hashing it before saving).
Summary
In summary, Django establishes a relationship between your custom form fields and the corresponding model fields through naming conventions and validation processes:
The field names in your form should match those in your model for automatic handling.
The Meta class specifies which model to use and which fields to include.
When processing form submissions, you manually map custom field values (like passwords) to their respective attributes on the model before saving.
This design allows for flexibility in defining forms while maintaining a clear connection to your underlying data models.
'''